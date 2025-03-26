import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# Load environment variables
load_dotenv()

# Disable SSL Verification
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.verify_mode = 0  # Disable SSL certificate verification
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)

# Set up session with SSL disabled
session = requests.Session()
session.mount("https://", SSLAdapter())

# Use OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")

# Define LLM with OpenRouter API (No OpenAI Key Needed)
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-lite-preview-02-05:free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1"
)
# Define a simple prompt
prompt = PromptTemplate(
    input_variables=["question"],
    template=f"Explain in detail: {input()}"
)

# Create a chain with the LLM
chain = prompt | llm
response = chain.invoke({"input": "How does OpenRouter work?"})

# Run the chain
print(response)
