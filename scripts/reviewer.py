import os
import json
import requests
import sys

# 1. Load the Data sent by GitHub
payload_json = sys.argv[1]
payload = json.loads(payload_json)

# 2. Setup GitHub Connection
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def post_comment(url, body):
    response = requests.post(url, json={"body": body}, headers=HEADERS)
    if response.status_code == 201:
        print(f"✅ Comment posted: {body}")
    else:
        print(f"❌ Failed to post comment: {response.text}")

# 3. Decision Logic
def run_gatekeeper():
    print("--- 🕵️ AI GATEKEEPER STARTING ---")
    
    # CHECK: Is this just a Ping?
    if "zen" in payload:
        print("✅ Received GitHub Ping! The connection is working.")
        return

    # CHECK: Is this a Pull Request?
    if "pull_request" not in payload:
        print("ℹ️ Not a Pull Request event. Skipping.")
        return

    # 4. Extract PR Details
    pr = payload["pull_request"]
    pr_title = pr["title"]
    user = pr["user"]["login"]
    comments_url = pr["comments_url"]
    
    print(f"📋 Reviewing PR: {pr_title} by @{user}")

    # 5. THE RULE CHECK (The "AI" Logic)
    # Simple Rule: Title must contain "feat" or "fix"
    if "feat" in pr_title.lower() or "fix" in pr_title.lower():
        msg = f"👋 Hi @{user}! I am the AI Gatekeeper.\n\n✅ **Approved:** Your title follows the standard naming convention."
        post_comment(comments_url, msg)
    else:
        msg = f"👋 Hi @{user}! I am the AI Gatekeeper.\n\n⚠️ **Changes Requested:** Your title '{pr_title}' is missing a tag.\nPlease rename it to start with `feat:` or `fix:`."
        post_comment(comments_url, msg)

if __name__ == "__main__":
    run_gatekeeper()