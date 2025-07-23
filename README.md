# GitHub Issue Analyzer

A simple website that uses a LLM to analyze a GitHub issue and return a structured JSON summary.

## Features
- Takes GitHub repo URL and issue number
- Uses 'moonshotai/Kimi-K2-Instruct:novita' for analysis
- Summarizes the issue
- Streamlit UI with JSON Output
- Caches results for speed

## Setup
```bash
# Clone and navigate
git clone https://github.com/Shreshtvg/Github_Issue_Analyser.git
cd github-issue-analyzer

# Create virtual Environment
python -m venv <your env name>

# Activate your env
<your env name>\Scripts\activate

# Install requirements and Packages
pip install -r requirements.txt

# Start backend
uvicorn backend.app:app --reload

# In new terminal, start frontend
streamlit run frontend/streamlit_ui.py

A page will open on the Browser. Enter github link and issue number and click on Analyse
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
