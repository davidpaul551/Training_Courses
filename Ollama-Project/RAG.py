import os
import requests
import faiss
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

load_dotenv(override=True)
# Step 1: Set up the GroqAPI configuration
api_key = load_dotenv("GROQ_API_KEY")
endpoint = "https://api.groq.com/openai/v1/chat/completions"
model = SentenceTransformer('all-MiniLM-L6-v2', use_auth_token=True)
requests.packages.urllib3.disable_warnings()
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Step 2: Load documents from the 'data' directory
data_dir = 'data'
documents = []
file_paths = []

for file_name in os.listdir(data_dir):
    file_path = os.path.join(data_dir, file_name)
    if os.path.isfile(file_path) and file_name.endswith('.txt'):
        file_paths.append(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            documents.append(file.read().strip())

print(f"Loaded {len(documents)} documents from {data_dir}")

# Step 3: Use a Sentence Transformer model to generate embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
document_embeddings = embedding_model.encode(documents, convert_to_tensor=True)

# Step 4: Set up FAISS for similarity search
dimension = document_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(document_embeddings.detach().numpy())

# Step 5: Perform retrieval based on the user's query
query = "Explain the importance of fast language models"
query_embedding = embedding_model.encode([query], convert_to_tensor=True).detach().numpy()

k = 2  # Number of relevant documents to retrieve
distances, indices = index.search(query_embedding, k)

# Retrieve relevant documents
retrieved_docs = [documents[i] for i in indices[0]]
context = " ".join(retrieved_docs)
print(f"Retrieved Context: {context}")

# Step 6: Send the retrieval-augmented prompt to GroqAPI
payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "user",
            "content": f"Using the following context: '{context}', Explain the importance of fast language models."
        }
    ]
}

response = requests.post(endpoint, headers=headers, json=payload, verify=False)

# Step 7: Handle the response
if response.status_code == 200:
    data = response.json()
    print("Generated Response:", data["choices"][0]["message"]["content"])
else:
    print(f"Error {response.status_code}: {response.text}")
