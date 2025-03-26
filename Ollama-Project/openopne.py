import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model selection
MODEL = "google/gemini-2.0-flash-001"

# Initialize LangChain OpenAI wrapper with OpenRouter API
llm = ChatOpenAI(
    model=MODEL,
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1"
)

# Define a prompt template
prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful assistant. Answer the following question: {question}"
)

# Create LLM chain
chain = prompt | llm

# Task definition
task = "What are the titles of some James Joyce books?"

# Invoke LangChain chain
response = chain.invoke({"question": task})

# Print response
print(response["text"])
