from typing import List, Type
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from chromadb.config import Settings
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
import chromadb
from config import Config
from models import BaseVectorEntry

class LlamaChromaDatabase:
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.client = chromadb.Client(Settings(chroma_api_impl="rest",
                                               chroma_server_host=Config.CHROMA_URL,
                                               chroma_server_http_port="8000"))
        
    def _get_collection_name(self, entry_type: Type[BaseVectorEntry]) -> str:
        return f"{Config.COLLECTION_PREFIX}_{entry_type.__name__}"

    def insert(self, entry: BaseVectorEntry) -> str:
        collection_name = self._get_collection_name(type(entry))
        collection = self.client.get_or_create_collection(name=collection_name)
        
        # Convert entry to dictionary
        entry_dict = entry.dict()
        
        # Insert the entry
        collection.add(
            documents=[entry_dict["content"]],
            metadatas=[{k: v for k, v in entry_dict.items() if k != "content"}],
            ids=[entry_dict["id"]]
        )
        
        return entry_dict["id"]

    def search(self, query: str, entry_type: Type[BaseVectorEntry], limit: int = 10) -> List[BaseVectorEntry]:
        collection_name = self._get_collection_name(entry_type)
        collection = self.client.get_or_create_collection(name=collection_name)
        
        results = collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        entries = []
        for i, doc in enumerate(results["documents"][0]):
            entry_dict = results["metadatas"][0][i]
            entry_dict["content"] = doc
            entries.append(entry_type(**entry_dict))
        
        return entries

    def update(self, id: str, entry: BaseVectorEntry) -> bool:
        collection_name = self._get_collection_name(type(entry))
        collection = self.client.get_or_create_collection(name=collection_name)
        
        entry_dict = entry.dict()
        
        collection.update(
            documents=[entry_dict["content"]],
            metadatas=[{k: v for k, v in entry_dict.items() if k != "content"}],
            ids=[id]
        )
        
        return True

    def delete(self, id: str, entry_type: Type[BaseVectorEntry]) -> bool:
        collection_name = self._get_collection_name(entry_type)
        collection = self.client.get_or_create_collection(name=collection_name)
        
        collection.delete(ids=[id])
        
        return True