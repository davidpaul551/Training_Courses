import requests
import os

from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, verify=False)

print(response.json())



endpoint = "https://api.groq.com/openai/v1/chat/completions"


model_id = 'llama3-70b-8192'

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
    }

payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "user",
            "content": "Explain the importance of fast language models"
        }
    ]
}

response = requests.post(endpoint, headers=headers, json=payload, verify=False)

if response.status_code == 200:
    data = response.json()
    print(data["choices"][0]["message"]["content"])
else:
    print(f"Error {response.status_code}: {response.text}")
