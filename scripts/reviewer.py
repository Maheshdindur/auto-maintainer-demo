import os
import json
import sys
import subprocess
import time

# --- 0. AUTO-INSTALL DEPENDENCIES ---
# We install these automatically so the Docker container has the tools it needs.
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
# We read the payload from the Environment Variable (Safe Mode)
payload_json = os.environ.get("GITHUB_PAYLOAD")
if not payload_json:
    print("❌ Critical Error: No GITHUB_PAYLOAD found. Is Kestra passing the env var?")
    sys.exit(1)

try:
    payload = json.loads(payload_json)
except json.JSONDecodeError:
    print("❌ Critical Error: GITHUB_PAYLOAD contains invalid JSON.")
    sys.exit(1)

# Get Keys from Docker Environment
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GITHUB_TOKEN or not GOOGLE_API_KEY:
    print("❌ Keys missing. Please check docker-compose.yml and restart Docker.")
    sys.exit(1)

# Configure the AI Model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp') 

# --- 2. HELPER FUNCTIONS ---

def get_pr_diff(diff_url):
    """
    Downloads the raw code changes (Diff) from GitHub.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        # This specific header tells GitHub "Give me the code diff, not the JSON"
        "Accept": "application/vnd.github.v3.diff" 
    }
    response = requests.get(diff_url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Failed to download Diff: {response.status_code}")
        return None
    return response.text

def post_comment(comments_url, body):
    """
    Posts the AI's final review to the GitHub Pull Request.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    # We add a small footer so people know it's a bot
    final_body = body + "\n\n_— Reviewed by OS-Maintainer Bot 🤖_"
    response = requests.post(comments_url, json={"body": final_body}, headers=headers)
    if response.status_code == 201:
        print("✅ Comment posted successfully.")
    else:
        print(f"❌ Failed to post comment: {response.text}")

def analyze_code_with_gemini(diff_text, pr_title, user):
    """
    Sends the code to Google Gemini for a 'Senior Developer' analysis.
    """
    # Safety: Truncate very large diffs to prevent API errors
    if len(diff_text) > 30000:
        diff_text = diff_text[:30000] + "\n... (Diff truncated due to size)"

    prompt = f"""
    You are 'OS-Maintainer', an expert Senior Software Engineer and Open Source Maintainer.
    
    Review the following Pull Request from user @{user}.
    
    **PR Title:** {pr_title}
    
    **Code Changes (Git Diff):**
    ```diff
    {diff_text}
    ```
    
    **Your Instructions:**
    1.  **Ignore formatting/style nitpicks.** Focus on Logic, Security, and Best Practices.
    2.  **Check for Bugs:** specific errors, potential crashes, or security leaks (like API keys).
    3.  **Be Helpful:** If the code is bad, explain *why* and give a code snippet to fix it.
    4.  **Verdict:** End with either '✅ **APPROVE**' or '⚠️ **REQUEST CHANGES**'.
    
    Provide your review in clear Markdown.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ **AI Error:** I encountered an error analyzing the code. ({str(e)})"

# --- 3. MAIN EXECUTION FLOW ---
def run():
    print("--- 🧠 AI BRAIN STARTING ---")

    # 1. Validation: Is this a PR event?
    if "pull_request" not in payload:
        print("ℹ️ Event is not a Pull Request. Skipping.")
        return

    # 2. Validation: Is the PR opened or updated?
    action = payload.get("action")
    if action not in ["opened", "reopened", "synchronize"]:
        print(f"ℹ️ Ignoring action '{action}'. Only reviewing new code.")
        return

    # 3. Extract Details (FIXED BUG HERE: removed incorrect nesting)
    pr = payload["pull_request"]
    pr_title = pr["title"]
    user = pr["user"]["login"]
    diff_url = pr["diff_url"]      # <--- This is the corrected path
    comments_url = pr["comments_url"]

    print(f"👀 Reviewing PR: '{pr_title}' by @{user}")

    # 4. Get the Code
    print("⬇️ Downloading Code Diff...")
    code_diff = get_pr_diff(diff_url)
    
    if not code_diff or not code_diff.strip():
        print("⚠️ Diff is empty. Maybe it's a binary file change? Skipping.")
        return

    # 5. Analyze with AI
    print("🤔 Thinking (Querying Gemini)...")
    review = analyze_code_with_gemini(code_diff, pr_title, user)

    # 6. Post Result
    print("🗣️ Posting Review to GitHub...")
    post_comment(comments_url, review)

if __name__ == "__main__":
    run()