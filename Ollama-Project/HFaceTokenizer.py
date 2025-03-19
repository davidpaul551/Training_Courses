from huggingface_hub import login
from transformers import AutoTokenizer
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Define model names as constants
META_LLAMA_MODEL = 'meta-llama/Meta-Llama-3.1-8B'
META_LLAMA_INSTRUCT_MODEL = 'meta-llama/Meta-Llama-3.1-8B-Instruct'
PHI3_MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
QWEN2_MODEL_NAME = "Qwen/Qwen2-7B-Instruct"
STARCODER2_MODEL_NAME = "bigcode/starcoder2-3b"

# Initialize a sample message for testing chat templates
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Tell a light-hearted joke for a room of Data Scientists"}
]

# Temporary workaround: Disable SSL verification globally for requests
requests.packages.urllib3.disable_warnings()  # Suppress SSL warnings
session = requests.Session()
session.verify = False  # Disable SSL verification

def authenticate_huggingface():
    """Authenticate using Hugging Face token from .env file."""
    hf_token = os.getenv('HF_TOKEN')
    if not hf_token:
        raise ValueError("HF_TOKEN not found in .env file. Please set it.")
    login(hf_token, add_to_git_credential=True)
    print("Authenticated successfully.")

def check_tokenizer(tokenizer, text: str):
    """Check the tokenizer with encoding and decoding operations."""
    print(f"\nChecking tokenizer: {tokenizer.name_or_path}")
    tokens = tokenizer.encode(text)
    print("Tokens:", tokens)
    print("Decoded:", tokenizer.decode(tokens))
    print("Batch Decoded:", tokenizer.batch_decode([tokens]))
    print("Added Vocabulary:", tokenizer.get_added_vocab())

def check_chat_template(tokenizer, messages):
    """Check the application of chat templates using the tokenizer."""
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    print(f"\nChat Template for {tokenizer.name_or_path}:\n{prompt}")

def test_starcoder2_tokenizer():
    """Test the StarCoder2 tokenizer with code-specific input."""
    code = """
    def hello_world(person):
        print("Hello", person)
    """
    # Use the custom session with SSL verification disabled
    starcoder2_tokenizer = AutoTokenizer.from_pretrained(
        STARCODER2_MODEL_NAME,
        trust_remote_code=True,
        use_auth_token=os.getenv('HF_TOKEN'),
        requests_session=session  # Pass the custom session
    )
    tokens = starcoder2_tokenizer.encode(code)
    print("\nStarCoder2 Tokenizer:")
    for token in tokens:
        print(f"{token} = {starcoder2_tokenizer.decode(token)}")

def main():
    """Main function to execute all tests."""
    authenticate_huggingface()

    # Text sample for encoding tests
    text = "I am excited to show Tokenizers in action to my LLM engineers"

    # Test Meta-Llama models
    meta_llama_tokenizer = AutoTokenizer.from_pretrained(
        META_LLAMA_MODEL,
        trust_remote_code=True,
        use_auth_token=os.getenv('HF_TOKEN'),
        requests_session=session
    )
    check_tokenizer(meta_llama_tokenizer, text)
    check_chat_template(meta_llama_tokenizer, messages)

    meta_llama_instruct_tokenizer = AutoTokenizer.from_pretrained(
        META_LLAMA_INSTRUCT_MODEL,
        trust_remote_code=True,
        use_auth_token=os.getenv('HF_TOKEN'),
        requests_session=session
    )
    check_chat_template(meta_llama_instruct_tokenizer, messages)

    # Test PHI3 tokenizer
    phi3_tokenizer = AutoTokenizer.from_pretrained(
        PHI3_MODEL_NAME,
        use_auth_token=os.getenv('HF_TOKEN'),
        requests_session=session
    )
    check_tokenizer(phi3_tokenizer, text)
    check_chat_template(phi3_tokenizer, messages)

    # Test Qwen2 tokenizer
    qwen2_tokenizer = AutoTokenizer.from_pretrained(
        QWEN2_MODEL_NAME,
        use_auth_token=os.getenv('HF_TOKEN'),
        requests_session=session
    )
    check_tokenizer(qwen2_tokenizer, text)
    check_chat_template(qwen2_tokenizer, messages)

    # Test StarCoder2 tokenizer with code input
    test_starcoder2_tokenizer()

if __name__ == "__main__":
    main()