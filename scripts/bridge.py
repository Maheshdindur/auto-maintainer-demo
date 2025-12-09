import sys
import os
import google.generativeai as genai

# CONFIG
IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', '.idea'}
ALLOWED_EXTENSIONS = {'.py', '.js', '.html', '.css', '.java', '.go', '.md'}

def get_context(path):
    """Reads a file or scans a folder context."""
    if os.path.isfile(path):
        with open(path, "r") as f:
            return f"--- FILE: {os.path.basename(path)} ---\n{f.read()}\n"
    
    # Folder Scan (For Contributor Mode)
    content = ""
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if any(f.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                try:
                    with open(os.path.join(root, f), "r") as f_read:
                        content += f"--- CONTEXT FILE: {f} ---\n{f_read.read()}\n\n"
                except: pass
    return content

def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: sys.exit(1)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # --- INPUT PARSING ---
    instruction = sys.argv[1]
    input_path = sys.argv[2]
    
    # MODE DETECTION
    mode = "FIX"
    output_path = input_path # Default: Overwrite the target (Fix Mode)
    
    if len(sys.argv) > 3:
        mode = "CONTRIBUTE"
        output_path = sys.argv[3] # New file path (Contribute Mode)

    print(f"--- MODE: {mode} ---")
    print(f"Instruction: {instruction}")

    # 1. READ CONTEXT
    context_data = get_context(input_path)

    # 2. PROMPT ENGINEERING (The "Authenticity Check")
    if mode == "FIX":
        prompt = (
            f"You are a Senior Maintainer Reviewing a Bug.\n"
            f"CODEBASE:\n```\n{context_data}\n```\n"
            f"ISSUE REPORT: {instruction}\n"
            f"TASK: \n"
            f"1. REVIEW: Does this code actually contain the issue described?\n"
            f"2. FIX: If yes, rewrite the code to fix it.\n"
            f"3. OUTPUT: Return ONLY the full fixed code. If the issue is invalid, return the original code unchanged."
        )
    else: # CONTRIBUTE MODE
        prompt = (
            f"You are an Open Source Contributor.\n"
            f"EXISTING PROJECT CONTEXT:\n```\n{context_data}\n```\n"
            f"CONTRIBUTION IDEA: {instruction}\n"
            f"TASK: Create a NEW file that adds this value to the project.\n"
            f"RULES: Follow the coding style of the context. Return ONLY the code for the new file."
        )

    # 3. GENERATE & WRITE
    try:
        print("--- AGENT THINKING ---")
        response = model.generate_content(prompt)
        new_code = response.text.replace("```python", "").replace("```", "").strip()
        
        # Ensure directory exists (for new contributions)
        if mode == "CONTRIBUTE":
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            f.write(new_code)
            
        print(f"--- SUCCESS: Wrote to {output_path} ---")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()