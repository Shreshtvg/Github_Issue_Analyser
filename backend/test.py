# backend/test_model.py

# Use when Model not working to debug

from model import analyze_issue

sample_prompt = """
You are an expert product analyst. Analyze the GitHub issue below and return the following JSON fields:
- summary (1 sentence)
- type: bug, feature_request, documentation, question, or other
- priority_score (1–5) with justification
- suggested_labels (2–3 tags)
- potential_impact (only if it's a bug)

Now analyze:
Title: App crashes on tab switch
Body: When switching tabs quickly between "Home" and "Profile", the app crashes instantly. This started after the recent update.
Comments:
- I'm facing the same issue.
- Happens every time I switch tabs fast.
- Only occurs on Android.

Respond with JSON only.
"""

if __name__ == "__main__":
    result = analyze_issue(sample_prompt)
    print("Response from LLM:")
    print(result)
