#extracts skills from pdf text

import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def extract_skills(text: str) -> list[str]:
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "resume-skill-extractor",
    }

    prompt = f"""
You are a skilled resume parser.
Return ONLY a JSON object with a key "skills" containing a list of strings.
Do not include any additional text.

{text}
"""

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()

    result = response.json()
    content = result["choices"][0]["message"]["content"]

    print("RAW LLM CONTENT:")
    print(repr(content))

    parsed_json = json.loads(content)
    return [skill.lower() for skill in parsed_json["skills"]]


    

