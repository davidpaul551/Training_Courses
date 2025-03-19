import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Get the HF_TOKEN value
HF_TOKEN = os.getenv("HF_TOKEN")


if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set. Please check your .env file and reload.")

print(f"HF_TOKEN loaded successfully: {HF_TOKEN[:5]}******")
