import os
import json
import sys
import subprocess
import time

# --- 0. AUTO-INSTALL DEPENDENCIES ---
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import requests
    import google.generativeai as genai
except ImportError:
    print("📦 Installing AI dependencies...")
    install("requests")
    install("google-generativeai")
    import requests
    import google.generativeai as genai

# --- 1. LOAD CONFIGURATION ---
payload_json = os.environ.get("GITHUB_PAYLOAD")
if not payload_json:
    print("❌ Critical Error: No GITHUB_PAYLOAD found.")
    sys.exit(1)

try:
    payload = json.loads(payload_json)
except json.JSONDecodeError:
    print("❌ Critical Error: GITHUB_PAYLOAD contains invalid JSON.")
    sys.exit(1)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GITHUB_TOKEN or not GOOGLE_API_KEY:
    print("❌ Keys missing. Check docker-compose.yml.")
    sys.exit(1)

# --- CHANGED: Use Stable Model for better Rate Limits ---
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') 

# --- 2. HELPER FUNCTIONS ---
def get_pr_diff(diff_url):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff" 
    }
    response = requests.get(diff_url, headers=headers)
    if response.status_code != 200:
        return None
    return response.text

def post_comment(comments_url, body):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    final_body = body + "\n\n_— Reviewed by OS-Maintainer Bot 🤖_"
    requests.post(comments_url, json={"body": final_body}, headers=headers)

def analyze_code_with_gemini(diff_text, pr_title, user):
    if len(diff_text) > 30000:
        diff_text = diff_text[:30000] + "\n... (Diff truncated)"

    prompt = f"""
    You are 'OS-Maintainer', a Senior Software Engineer.
    Review PR from @{user}. Title: {pr_title}
    
    Code Changes:
    ```diff
    {diff_text}
    ```
    
    Instructions:
    1. Check for **Security Leaks** (passwords/keys) and **Logic Bugs**.
    2. Be helpful and provide code fixes.
    3. Verdict: '✅ **APPROVE**' or '⚠️ **REQUEST CHANGES**'.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ **AI Error:** {str(e)}"

# --- 3. MAIN EXECUTION ---
def run():
    if "pull_request" not in payload: return
    action = payload.get("action")
    if action not in ["opened", "reopened", "synchronize"]: return

    pr = payload["pull_request"]
    diff_url = pr["diff_url"]
    comments_url = pr["comments_url"]

    # Download Code
    code_diff = get_pr_diff(diff_url)
    if not code_diff: return

    # Analyze
    review = analyze_code_with_gemini(code_diff, pr["title"], pr["user"]["login"])

    # Post
    post_comment(comments_url, review)

if __name__ == "__main__":
    run()