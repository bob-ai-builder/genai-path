git init
git add llm_chat.py .gitignore README.md
git status                   # .env must NOT be listed
git commit -m "Phase 1: llm_chat.py"

# Option A — GitHub CLI
gh repo create genai-path --public --source=. --push

# Option B — create an empty repo on github.com first, then:
git remote add origin https://github.com/bob-ai-builder/genai-path.git
git branch -M main
git push -u origin main