from fastapi import FastAPI
from pydantic import BaseModel
from backend.utils import fetch_issue_data, build_prompt, cache_result, get_cached_result
from backend.model import analyze_issue
import hashlib

app = FastAPI()

class IssueInput(BaseModel):
    repo_url: str
    issue_number: int

@app.post("/analyze")
def analyze(input: IssueInput):
    print("Inside Backend")
    key = hashlib.md5(f"{input.repo_url}-{input.issue_number}".encode()).hexdigest()

    cached = get_cached_result(key)
    if cached:
        print("Returning cached result")
        return {"cached": True, "result": cached}

    print("Sending to fetch data")
    data = fetch_issue_data(input.repo_url, input.issue_number)

    if "error1" in data:
        # print("Issue number not valid in repo:", data["error"])
        return {"error": data["error1"]}
    if "error2" in data:
        return {"error": data["error2"]}

    prompt = build_prompt(data)
    print("Prompt received")
    result = analyze_issue(prompt)

    if "error2" in result:
        print("Error in model response:", result["error2"])
        return {"error": result["error2"]}
    if "error3" in result:
        print("Error in analysis:", result["error3"])
        return {"error": "Enter the Access Token in backend/.env file."}

    cache_result(key, result["response"])
    print("Result from LLM:", result["response"])
    return {"cached": False, "result": result["response"]}
