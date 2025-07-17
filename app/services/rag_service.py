from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Global vars to hold vector store and embeddings
# This is a simple in-mem cache. In production, need to persist this.
vector_store = None
embeddings = None

def load_and_build_vector_store(directory_path: str = "data/"):
    """
    Loads documents, splits them, creates embeddings, and builds a vector store.
    This function is designed to be called once during application startup.
    """
    global vector_store, embeddings

    if vector_store is not None:
        print("Vector store already loaded.")
        return
    
    print("--- Building a new vector store from PDF resumes ---")

    # 1. Load documents from the specified directory
    loader = PyPDFDirectoryLoader(directory_path)
    documents = loader.load()
    if not documents:
        raise ValueError(f"No documents found in directory: {directory_path}")
    
    # 2. Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # 3. Create embeddings
    # Use Google's embedding model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # 4. Create the FAISS vector store from the documents and embeddings
    vector_store = FAISS.from_documents(docs, embeddings)

    print("--- Vector store built successfully! ---")


def get_retriever():
    """
    Returns a retriever object from the global vertor store.
    Ensures the store is loaded before returning.
    """
    global vector_store
    if vector_store is None:
        load_and_build_vector_store()
    return vector_store.as_retriever()


def create_rag_chain():
    """
    Creates the conversational RAG chain for querying resumes.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                                 google_api_key=google_api_key,
                                 temperature=0.1)
    retriever = get_retriever()

    # This prompt is key. It instructs the LLM on how to use the retrieved context.
    prompt = ChatPromptTemplate.from_template("""
    You are an expert HR assisant. Your task is to answer questions about a pool of candidates based on their resumes.
    Use the following retrieved resume context to answer the question.
    If you don't know the answer from the context provided, just say that you don't know.
    Don't make up information. Be concise and professional.

    Context:
    {context}

    Question:
    {input}

    Answer:
    """)

    # This chain will take a question and the retrieved documents and generate an answer.
    document_chain = create_stuff_documents_chain(llm, prompt)

    # This is the main chain that orchestrates everything.
    # It takes the user's question, passes it to the retriever to get relevant docs,
    # and then passes the question and docs to the document_chain.
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain

def create_text_rag_chain(text: str):
    """
    Creates a temporary, in-memory RAG chain for a specific piece of text.
    """
    print("--- Creating temporary RAG chain for specific text ---")

    # 1. Split the provided text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.create_documents([text]) # create_documents expects a list

    # 2. Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    # 3. Create a temporary, in-memory vector store from this one document
    temp_vector_store = FAISS.from_documents(docs, embeddings)
    temp_retriever = temp_vector_store.as_retriever()

    # 4. Use the same prompt and LLM as our other RAG chain
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                                 google_api_key=google_api_key,
                                 temperature=0.1)
    prompt = ChatPromptTemplate.from_template("""
    You are an expert analyst. Use the following retrieved context to answer the question.
    If you don't know the answer, just say that. Be concise.

    Context: {context}
    Question: {input}
    Answer:
    """)
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(temp_retriever, document_chain)
    
    return retrieval_chain