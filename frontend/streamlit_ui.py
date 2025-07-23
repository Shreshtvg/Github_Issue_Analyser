import streamlit as st
import requests
import pyperclip

def repo_exists(repo_url: str) -> bool:
    """Check if the given GitHub repository exists."""
    try:
        # Extract owner and repo name from URL
        parts = repo_url.strip().rstrip('/').split('/')
        owner, repo = parts[-2], parts[-1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        response = requests.get(api_url)
        return response.status_code == 200
    except Exception:
        return False

st.set_page_config(page_title="GitHub Issue Analyzer", layout="centered")
st.title("🔍 GitHub Issue Analyzer with AI")

repo_url = st.text_input("GitHub Repository URL", placeholder="Paste the GitHub URL")
issue_number_input = st.text_input("Issue Number", placeholder="Enter the Issue Number")

if st.button("Analyze Issue"):
    if not repo_url:
        st.error("❌ Please enter a GitHub repository URL.")
    elif not repo_exists(repo_url):
        st.error("❌ This repository does not exist on GitHub.")
    elif not issue_number_input.strip().isdigit() or issue_number_input == "0":
        st.error("❌ Please enter a valid Issue number.")
    else:
        issue_number = int(issue_number_input)
        with st.spinner("Analyzing issue..."):
            try:
                res = requests.post("http://localhost:8000/analyze", json={
                    "repo_url": repo_url.strip(),
                    "issue_number": issue_number
                })
                res.raise_for_status()
                data = res.json()
                result = data["result"]
                st.json(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")