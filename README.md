# 🛡️ OS-Maintainer: The AI Gatekeeper

> **The Safe, Dual-Mode Autonomous Maintainer for Open Source.**
> *Powered by Kestra, Docker, and Google Gemini.*

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Tech Stack](https://img.shields.io/badge/Stack-Kestra%20|%20Docker%20|%20Python-blue)
![AI Model](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)

## 🚨 The Problem
Open Source maintainers face overwhelming volumes of Pull Requests (PRs), leading to burnout and missed security vulnerabilities. Manual code review is slow, inconsistent, and often fails to catch subtle policy violations (like misformatted commit messages) or critical security flaws (like hardcoded secrets)

## 🤖 The Solution
**OS-Maintainer** is an autonomous AI agent that acts as a **First-Line Gatekeeper**. It listens to repository events 24/7, analyzes incoming code, and enforces contribution rules automatically.

Unlike generic coding bots, OS-Maintainer is designed for **Safety and Trust**:
* It does not blindly merge code.
* It acts as a "Senior Reviewer," requesting changes when rules are violated.
* It runs locally in a secure Docker sandbox.

## ⚙️ Architecture

1.  **The Ears (Ngrok + Webhooks):**GitHub sends real-time events (PR Open, Push) to the public Ngrok endpoint.
2.  **The Nervous System (Kestra):** Kestra's Webhook Trigger immediately catches the event and launches the AI analysis flow, providing full auditability of the entire process.Orchestrates the workflow, managing inputs, triggers, and execution flow.
3.  **The Brain (Google Gemini 2.5):** The Kestra flow executes a containerized Python script which calls the Gemini API to analyze the PR's Diff, title, and existing contribution rules.
4.  **The Voice (GitHub API):** Based on the AI's decisive verdict, the system posts semantic comments and sets the appropriate GitHub Status Check (e.g., green check or red X) to enforce the policy.
## 🚀 Key Features

* **⚡ Instant Event Detection:** Wakes up immediately when a PR is opened.
* **🧠 Semantic Analysis:** Verifies code and commit messages against project conventions (feat:, fix:, etc.).
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
