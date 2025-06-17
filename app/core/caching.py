import langchain
from langchain_community.cache import SQLiteCache

def setup_langchain_cache():
    """
    Sets up a global SQLite cache for all LangChain LLM calls.
    This significantly speeds up repeated requests with the same prompt.
    """
    print("--- Setting up LangChain global cache ---")
    langchain.llm_cache = SQLiteCache(database_path=".langchain.db")
    print("Cache setup complete.")