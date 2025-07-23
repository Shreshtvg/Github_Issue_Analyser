# backend/model.py

import os
import json
import requests
from dotenv import load_dotenv

API_URL = "https://router.huggingface.co/v1/chat/completions"

def analyze_issue(prompt: str) -> dict:
    print("Sending prompt to LLM for analysis...")
    load_dotenv()
    HF_TOKEN = os.getenv("HF_TOKEN")

    HEADERS = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        payload = {
            "model": "moonshotai/Kimi-K2-Instruct:novita",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return {"error": "No response from model."}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
