# 🛡️ OS-Maintainer: The AI Gatekeeper

> **The Safe, Dual-Mode Autonomous Maintainer for Open Source.**
> *Powered by Kestra, Docker, and Google Gemini.*

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Tech Stack](https://img.shields.io/badge/Stack-Kestra%20|%20Docker%20|%20Python-blue)
![AI Model](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)

## 🚨 The Problem
Open Source maintainers are burning out. Thousands of Pull Requests (PRs) go unreviewed because maintainers lack the time to manually check every single contribution. Bad PRs clutter the repo, while good ideas die in the backlog.

## 🤖 The Solution
**OS-Maintainer** is an autonomous AI agent that acts as a **First-Line Gatekeeper**. It listens to repository events 24/7, analyzes incoming code, and enforces contribution rules automatically.

Unlike generic coding bots, OS-Maintainer is designed for **Safety and Trust**:
* It does not blindly merge code.
* It acts as a "Senior Reviewer," requesting changes when rules are violated.
* It runs locally in a secure Docker sandbox.

## ⚙️ Architecture

1.  **The Ears (Ngrok + Webhooks):** Listens for real-time GitHub events (Open PR, Comment, Push).
2.  **The Nervous System (Kestra):** Orchestrates the workflow, managing inputs, triggers, and execution flow.
3.  **The Brain (Google Gemini 2.5):** Analyzes the context (PR Title, Diff, Rules) to make intelligent decisions.
4.  **The Voice (GitHub API):** Posts semantic comments directly to the PR (Approvals or Change Requests).

## 🚀 Key Features

* **⚡ Instant Event Detection:** Wakes up immediately when a PR is opened.
* **🧠 Semantic Analysis:** Understands if a PR(code) follows conventions.
* **💬 Automated Feedback:** Posts friendly, constructive comments to contributors.
* **🔒 Secure Execution:** Runs entirely within a Docker container; secrets are never exposed to the AI model.

## 🛠️ Installation & Setup

### Prerequisites
* Docker & Docker Compose
* Ngrok (for local testing)
* GitHub Account (Personal Access Token)
* Google Gemini API Key

### Quick Start

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/Maheshdindur/auto-maintainer-demo.git](https://github.com/Maheshdindur/auto-maintainer-demo.git)
    cd auto-maintainer-demo
    ```

2.  **Configure Environment**
    Update `docker-compose.yml` with your API Keys (Google & GitHub).

3.  **Launch the Brain**
    ```bash
    docker compose up -d
    ```

4.  **Open the Tunnel**
    ```bash
    ngrok http 8080
    ```
    *Add the generated URL to your GitHub Repository Webhooks.*

## 🧪 Usage

1.  Create a new Branch: `git checkout -b feature/test-bot`
2.  Make changes and Push: `git push origin feature/test-bot`
3.  Open a Pull Request on GitHub.
4.  **Watch the Magic:** The OS-Maintainer will automatically comment on your PR within seconds!

---
*Built for the 2025 AI Hackathon.*
