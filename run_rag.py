import os
from dotenv import load_dotenv
from app.services.rag_service import load_and_build_vector_store, create_rag_chain

def main():
    # Load environment variables
    load_dotenv()
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY not found in .env file.")
    
    print("--- Initializing RAG Q&A System ---")

    # 1. Load resumes and build the vector store
    # This should only happen once when the application starts
    load_and_build_vector_store()
    
    # 2. Create the RAG chain
    rag_chain = create_rag_chain()
    
    # 3. Ask some questions!
    print("\n--- Ready to answer questions about candidates. ---")
    
    questions = [
        "Which candidate has experience with Docker and cloud services?",
        "How many years of experience does John Doe have?",
        "Who is more junior and has experience with Flask?",
        "Is there a candidate with experience in project management?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        response = rag_chain.invoke({"input": question})
        print(f"✅ Answer: {response['answer']}")


if __name__ == "__main__":
    main()