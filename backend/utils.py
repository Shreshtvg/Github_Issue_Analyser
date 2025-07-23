import requests
import os
import json
from pathlib import Path

#creates cache directory for results
CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

GITHUB_API = "https://api.github.com/repos"

def fetch_issue_data(repo_url: str, issue_number: int) -> dict:
    try:
        parts = repo_url.rstrip("/").split("/")[-2:]
        owner, repo = parts[0], parts[1]
        issue_url = f"{GITHUB_API}/{owner}/{repo}/issues/{issue_number}"
        comments_url = f"{GITHUB_API}/{owner}/{repo}/issues/{issue_number}/comments"

        issue = requests.get(issue_url).json()
        comments = requests.get(comments_url).json()

        return {
            "title": issue.get("title", ""),
            "body": issue.get("body", ""),
            "comments": [c.get("body", "") for c in comments if c.get("body")]
        }
    except Exception as e:
        print("fetch function error:")
        return {"error": str(e)}

def build_prompt(data: dict) -> str:
    example = '''Example:
{
  "summary": "User experiences crash when switching tabs quickly.",
  "type": "bug",
  "priority_score": "4 - Affects many users and breaks expected functionality.",
  "suggested_labels": ["bug", "UI", "high-priority"],
  "potential_impact": "Users may experience crashes during regular usage."
}'''

    comments_summary = "\n- ".join(data['comments'][:3]) if data['comments'] else "No comments."
    body_snippet = (data['body'][:800] + "...") if len(data['body']) > 800 else data['body']

    prompt = f"""
You are an expert product analyst. Analyze the GitHub issue below and return the following JSON fields:
- summary (1 sentence)
- type: bug, feature_request, documentation, question, or other
- priority_score (1–5) with justification
- suggested_labels (2–3 tags)
- potential_impact (only if it's a bug)

{example}

Now analyze:
Title: {data['title']}
Body: {body_snippet}
Comments:
- {comments_summary}

Respond with JSON only.
"""
    return prompt.strip()

def cache_result(key: str, result: str):
    with open(CACHE_DIR / f"{key}.json", "w", encoding="utf-8") as f:
        json.dump({"result": result}, f)

def get_cached_result(key: str) -> str | None:
    path = CACHE_DIR / f"{key}.json"
    if not path.exists():
        return None

    # Check if file is empty
    if path.stat().st_size == 0:
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("result")
    except json.JSONDecodeError:
        return None
