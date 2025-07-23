from fastapi import FastAPI, Request
from pydantic import BaseModel
from backend.utils import fetch_issue_data, build_prompt, cache_result, get_cached_result
from backend.model import analyze_issue
import hashlib

app = FastAPI()

#defining the type of parameters we expect in the request
class IssueInput(BaseModel):
    repo_url: str
    issue_number: int

@app.post("/analyze")
def analyze(input: IssueInput):
    key = hashlib.md5(f"{input.repo_url}-{input.issue_number}".encode()).hexdigest()
    cached = get_cached_result(key)
    if cached:
        return {"cached": True, "result": cached}

    data = fetch_issue_data(input.repo_url, input.issue_number)
    if "error" in data:
        return {"error": data["error"]}

    prompt = build_prompt(data)
    result = analyze_issue(prompt)
    cache_result(key, result)
    print("Result from LLM:", result)
    return {"cached": False, "result": result}


