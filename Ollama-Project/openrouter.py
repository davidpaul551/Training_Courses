import requests
import os
from dotenv import load_dotenv
import certifi

load_dotenv(override=True)

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("Missing API key. Please set OPENROUTER_API_KEY in your environment variables.")

url = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"

HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

def get_chat_completion(prompt: str):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload, verify=False)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"

# Example usage
if __name__ == "__main__":
    prompt = "Explain the importance of fast language models"
    print(get_chat_completion(prompt))
