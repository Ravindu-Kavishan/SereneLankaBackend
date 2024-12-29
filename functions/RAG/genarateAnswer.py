import os
import shutil
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from langchain_chroma import Chroma
# from langchain_google_genai import ChatGoogleGenerativeAI

DATA_PATH = os.path.join(os.getcwd(),"functions","RAG", "data", "tourism of sriLanka.pdf")

# Path to the PDF file and Chroma DB directory
# DATA_PATH = "data/Sigiriya.pdf"  # Replace with the actual path to your PDF file
persist_directory = "./chromadb"  # Path to persist the Chroma DB

# Configure Google Generative AI API
genai.configure(api_key="AIzaSyDLrw2Yg63sfzmfB0shnrSUt9GwvanUS7c")  # Replace with your API key


class GoogleGenerativeAIEmbeddings(Embeddings):
    """Custom embedding class using Google Generative AI."""

    def embed_documents(self, texts):
        """Generate embeddings for a list of documents."""
        return [
            genai.embed_content(model="models/text-embedding-004", content=text)["embedding"]
            for text in texts
        ]

    def embed_query(self, text):
        """Generate an embedding for a single query."""
        return genai.embed_content(model="models/text-embedding-004", content=text)["embedding"]


# Load Documents
def load_documents():
    loader = PyPDFLoader(DATA_PATH)
    documents = loader.load()
    if not documents:
        print("No content found in the PDF.")
    return documents


# Split Documents into Chunks
def chunking():
    data = load_documents()
    if not data:
        return []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    return text_splitter.split_documents(data)


# Initialize or Load Chroma DB
def get_existing_db():
    embedding_function = GoogleGenerativeAIEmbeddings()
    if os.path.exists(persist_directory):
        print("Chroma DB exists. Loading it...")
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_function,
        )
    else:
        print("No existing Chroma DB found. Creating a new one...")
        vectorstore = Chroma.from_documents(
            documents=chunking(),
            embedding=embedding_function,
            persist_directory=persist_directory,
        )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})
    return retriever


# Create a New Chroma DB
def create_new_db():
    embedding_function = GoogleGenerativeAIEmbeddings()
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    vectorstore = Chroma.from_documents(
        documents=chunking(),
        embedding=embedding_function,
        persist_directory=persist_directory,
    )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})
    return retriever


# # Ask a Question
# def ask_question(question):
#     retriever = get_existing_db()
#     results = retriever.invoke(question)
#     if results:
#         return results[0].page_content  # Return the most relevant result
#     return "No relevant answer found."


# Ask a Question
def ask_question(question):
    retriever = get_existing_db()  # Load or initialize the Chroma retriever
    results = retriever.invoke(question)  # Retrieve relevant results
    if results and len(results) >= 2:
        # Join the top 2 relevant results with a newline
        return "\n".join([result.page_content for result in results[:2]])
    elif results:
        # If less than 2 results are found, join all available results with a newline
        return "\n".join([result.page_content for result in results])
    return "No relevant answer found."


