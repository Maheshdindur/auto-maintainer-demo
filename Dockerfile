FROM kestra/kestra:latest

USER root

# 1. Install System Tools
RUN apt-get update && \
    apt-get install -y curl git python3-pip

# 2. CRITICAL: Upgrade pip and Force-Install Latest Gemini SDK
# We use --upgrade to ensure we don't get a stale, cached version.
RUN pip3 install --upgrade pip && \
    pip3 install --upgrade google-generativeai

# 3. Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*