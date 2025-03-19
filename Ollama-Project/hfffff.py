import os
import requests
import urllib3
from transformers import AutoTokenizer
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

# Constants
STARCODER2_MODEL_NAME = "bigcode/starcoder2-3b"

# Set up a resilient HTTP session with retry strategy
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

# Verify Hugging Face authentication token
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set. Please set it before running.")

def test_starcoder2_tokenizer():
    """
    Test the StarCoder2 tokenizer with code-specific input.
    Ensures proper SSL verification and handles request failures gracefully.
    """
    try:
        # Load tokenizer with authentication and error handling
        starcoder2_tokenizer = AutoTokenizer.from_pretrained(
            STARCODER2_MODEL_NAME,
            trust_remote_code=True,
            use_auth_token=HF_TOKEN,
            requests_session=session  # Optimized session with retries
        )

        # Test input
        code = """def hello_world(person):\n    print("Hello", person)"""
        tokens = starcoder2_tokenizer.encode(code, return_tensors="pt")

        assert tokens is not None, "Tokenization failed: No tokens returned."
        print("Tokenizer test passed ✅")

    except requests.exceptions.SSLError:
        raise RuntimeError("SSL Certificate Verification Failed! Please update your SSL certificates.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error while fetching tokenizer: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_starcoder2_tokenizer()
