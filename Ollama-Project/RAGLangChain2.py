# Imports
import os
import glob
import requests
from dotenv import load_dotenv
import gradio as gr

# Langchain Imports
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')

# Model and Vector Database Name
MODEL = "llama-3.3-70b-versatile"
db_name = "vector_db"

# Load Documents from Knowledge Base
folders = glob.glob("knowledge-base/*")

text_loader_kwargs = {'encoding': 'utf-8'}
documents = []
for folder in folders:
    doc_type = os.path.basename(folder)
    loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    folder_docs = loader.load()
    for doc in folder_docs:
        doc.metadata["doc_type"] = doc_type
        documents.append(doc)

# Split Documents into Chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# Create Embeddings and Vector Store
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embedding)

# Define Custom GroqAPI Class
class GroqAPI(LLM):
    def _call(self, prompt: str, stop=None) -> str:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}]
            },
            headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"}
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]

    @property
    def _identifying_params(self):
        return {"model": MODEL}

    @property
    def _llm_type(self) -> str:
        return "groqapi"

# Configure RetrievalQA Chain
llm = GroqAPI()
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Gradio Chat Function
def chat(query: str) -> str:
    response = qa.run(query)
    return response

# Gradio Interface
interface = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(lines=2, placeholder="Ask me a question about Insurellm..."),
    outputs="text",
    title="Insurellm QA Bot"
)

# Launch the Interface
interface.launch()
