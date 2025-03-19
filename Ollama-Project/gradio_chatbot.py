import gradio as gr
import ollama

system_message = "You are a helpful assistant."

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    stream = ollama.chat(model="llama3.2", messages=messages, stream=True)
    response = ""
    for chunk in stream:
        response += chunk["message"]["content"] or ''
        yield response

gr.ChatInterface(fn=chat, type="messages").launch()