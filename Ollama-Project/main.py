import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


API_URL = "http://localhost:11434/api/generate"

# MODEL_NAME = os.getenv("MODEL_NAME")

# HEADERS  = {
#     "Content-Type" : "application/json"
# }

# PROMPT = "Give me a suggestion about learning AI"

# PAYLOAD = {
#     "model":MODEL_NAME,
#     "prompt":PROMPT,
#     "stream":False
# }

# response = requests.post(API_URL, headers=HEADERS , json=PAYLOAD)

# if response.status_code == 200:
#     data = response.json()
#     print("AI response is ", data.get("response" , "No response is generated"))
# else:
#     print(response.status_code , response.text)



# Adversarial interaction between Models 

import requests

conversation = [
    {"role": "system", "content": "You are an AI debating system. Provide logical and well-argued responses."},
    {"role": "user", "content": "Is AI dangerous?"}
]
models = ["llama3.2","gemma:2b"]

def generate_resp(model_name, conversation_history):
    """Send a request to the local Ollama API"""
    PAYLOAD = {
        "model": model_name,
        "messages": conversation_history[-3:],
        "stream": False
    }

    HEADERS = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("http://localhost:11434/api/chat", json=PAYLOAD, headers=HEADERS, timeout=300)
        # print(f"🔍 Response status: {response.status_code}")
        # print(f"🔍 Response content: {response.text}")

        if response.status_code == 200:
            data = response.json()
            return data.get("message", {}).get("content", "⚠️ No content found")
        else:
            return f"Error: {response.status_code}, {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

# rep = generate_resp("gemma:2b", conversation)
# print(rep)
for i in range(3):
    current_model = models[i % 2]

    print(f"🤖 {current_model} is responding...")

    response = generate_resp(current_model, conversation)
    print(f"📝 {current_model}:", response)

    conversation.append({"role": "assistant", "content": response})

    if i < 2:
        adversarial_input = f"Counterargument: {response}"
        conversation.append({"role": "user", "content": adversarial_input})
