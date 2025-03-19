import os
import numpy as np
from sklearn.manifold import TSNE
import plotly.graph_objs as go
from langchain.embeddings import GroqAPIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Define the directory for the Chroma vector store
db_name = "chroma_db"

# Initialize GroqAPI Embeddings
embeddings = GroqAPIEmbeddings(model="gpt-4o-mini")

# Check if a Chroma Datastore already exists - if so, delete the collection to start from scratch
if os.path.exists(db_name):
    vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)
    vectorstore.delete_collection()

# Sample document chunks (Replace this with your actual document chunks)
chunks = [
    {"content": "Our products are top-notch.", "metadata": {"doc_type": "products"}},
    {"content": "Meet our amazing employees.", "metadata": {"doc_type": "employees"}},
    {"content": "The new contract terms are beneficial.", "metadata": {"doc_type": "contracts"}},
    {"content": "Our company is growing rapidly.", "metadata": {"doc_type": "company"}}
]

# Create the vector store using GroqAPI embeddings
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=db_name
)
print(f"Vectorstore created with {vectorstore._collection.count()} documents")

# Check the dimensionality of the embeddings
collection = vectorstore._collection
sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
dimensions = len(sample_embedding)
print(f"The vectors have {dimensions:,} dimensions")

# Preprocessing for Visualization
result = collection.get(include=['embeddings', 'documents', 'metadatas'])
vectors = np.array(result['embeddings'])
documents = result['documents']
doc_types = [metadata['doc_type'] for metadata in result['metadatas']]
colors = [['blue', 'green', 'red', 'orange'][['products', 'employees', 'contracts', 'company'].index(t)] for t in doc_types]

# 2D Visualization with t-SNE
tsne = TSNE(n_components=2, random_state=42)
reduced_vectors = tsne.fit_transform(vectors)

fig = go.Figure(data=[go.Scatter(
    x=reduced_vectors[:, 0],
    y=reduced_vectors[:, 1],
    mode='markers',
    marker=dict(size=5, color=colors, opacity=0.8),
    text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
    hoverinfo='text'
)])

fig.update_layout(
    title='2D Chroma Vector Store Visualization',
    width=800,
    height=600,
    margin=dict(r=20, b=10, l=10, t=40)
)

fig.show()

# 3D Visualization with t-SNE
tsne = TSNE(n_components=3, random_state=42)
reduced_vectors = tsne.fit_transform(vectors)

fig = go.Figure(data=[go.Scatter3d(
    x=reduced_vectors[:, 0],
    y=reduced_vectors[:, 1],
    z=reduced_vectors[:, 2],
    mode='markers',
    marker=dict(size=5, color=colors, opacity=0.8),
    text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
    hoverinfo='text'
)])

fig.update_layout(
    title='3D Chroma Vector Store Visualization',
    scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
    width=900,
    height=700,
    margin=dict(r=20, b=10, l=10, t=40)
)

fig.show()

# Setting up the RetrievalQA chain with GroqAPI
qa_chain = RetrievalQA.from_chain_type(
    llm=embeddings,  # Using GroqAPI embeddings
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Example query for RetrievalQA
query = "What are the benefits of our new contract?"
response = qa_chain.run(query)
print("Response from QA Chain:", response)
