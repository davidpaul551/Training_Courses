import os
import glob
import requests
from dotenv import load_dotenv
import gradio as gr


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

endpoint = "https://api.groq.com/openai/v1/chat/completions"
model_id = 'llama3-70b-8192'
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

system_message = "You are an expert in answering accurate questions about Insurellm, the Insurance Tech company. Give brief, accurate answers. If you don't know the answer, say so. Do not make anything up if you haven't been provided with relevant context."


context = {}


employees = glob.glob("knowledge-base/employees/*")
for employee in employees:
    name = os.path.basename(employee)[:-3]
    with open(employee , "r" , encoding="utf-8") as f:
        context[name] = f.read()


products = glob.glob("knowledge-base/employees/*")
for product in products:
    name = os.path.basename(product)[:-3]
    with open(product, "r", encoding="utf-8") as f:
        context[name] = f.read()

def get_relevant_context(message:str) -> list:
    relevant_context = []
    for context_title , context_details in context.items():
        if context_title.lower() in message.lower():
            relevant_context.append(context_details)
    return relevant_context


def add_context(message:str):
    relevant_context = get_relevant_context(message)
    if relevant_context:
        message+="\n\nThe following additional context might be relevant in answering this question:\n\n"
        for relevant in relevant_context:
            message += relevant+"\n\n"
    return message


def chat(message:str, history:list):
    messages = [
        {"role":"system","content":system_message}
        ]+history
    
    message = add_context(message)
    messages.append({"role":"user", "content":message})
    
    payload = {
        "model":model_id,
        "messages":messages
    }
    
    response = requests.post(endpoint,headers=headers , json=payload, verify=False)
    
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["messages"]["content"]
    else:
        return  f"Error {response.status_code}: {response.text}"


history =[]
user_message = "Who is Alex"

response = chat(user_message,history)
print("Response : ", response)

gr.ChatInterface(fn=chat).launch()