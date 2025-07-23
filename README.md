# GitHub Issue Analyzer

A simple app that uses a local LLM to analyze a GitHub issue and return a structured JSON summary.

## Features
- Takes GitHub repo URL and issue number
- Uses Ollama's local LLM (LLaMA 3) for analysis
- Summarizes, classifies, and labels the issue
- Streamlit UI with JSON copy button
- Caches results for speed

## Setup
```bash
# Clone and navigate
git clone <repo>
cd github-issue-analyzer

# Start backend
uvicorn app.app:app --reload

# In new terminal, start frontend
streamlit run ui/streamlit_ui.py
```

## Sample Output
```json
{
  "summary": "User requests support for nested dynamic imports in bundler.",
  "type": "feature_request",
  "priority_score": "3 - Requested by several users but not urgent.",
  "suggested_labels": ["feature", "build-system"],
  "potential_impact": ""
}