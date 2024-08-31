import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WEAVIATE_URL = os.getenv("WEAVIATE_URL")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
    CHROMA_URL = os.getenv("CHROMA_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_SERVICE = os.getenv("EMBEDDING_SERVICE", "openai")
    VECTOR_DB = os.getenv("VECTOR_DB", "weaviate")
    COLLECTION_PREFIX = os.getenv("COLLECTION_PREFIX", "datagpt")
    CLASS_PREFIX = os.getenv("CLASS_PREFIX", "DataGPT")