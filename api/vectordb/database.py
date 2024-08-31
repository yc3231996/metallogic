from abc import ABC, abstractmethod

class VectorDatabase(ABC):
    @abstractmethod
    def insert(self, entry):
        pass

    @abstractmethod
    def search(self, query, entry_type, limit=10):
        pass

    @abstractmethod
    def update(self, id, entry):
        pass

    @abstractmethod
    def delete(self, id, entry_type):
        pass



# database/llama_weaviate.py
from llama_index.vector_stores import WeaviateVectorStore
from llama_index import VectorStoreIndex, ServiceContext
from config import Config

class LlamaWeaviateDatabase(VectorDatabase):
    def __init__(self, embedding_service):
        self.vector_store = WeaviateVectorStore(
            weaviate_url=Config.WEAVIATE_URL,
            auth_client_secret=Config.WEAVIATE_API_KEY,
            index_name="VectorIndex"
        )
        self.service_context = ServiceContext.from_defaults(embed_model=embedding_service)
        self.index = VectorStoreIndex.from_vector_store(self.vector_store, service_context=self.service_context)

    def insert(self, entry):
        document = entry.to_document()
        self.index.insert(document)
        return document.doc_id

    def search(self, query, entry_type, limit=10):
        query_engine = self.index.as_query_engine(similarity_top_k=limit)
        results = query_engine.query(query)
        return [entry_type.from_node(node) for node in results.source_nodes]

    def update(self, id, entry):
        self.delete(id, type(entry))
        return self.insert(entry)

    def delete(self, id, entry_type):
        self.vector_store.delete(id)



# database/llama_chroma.py
from llama_index.vector_stores import ChromaVectorStore
from llama_index import VectorStoreIndex, ServiceContext
from config import Config
import chromadb

class LlamaChromaDatabase(VectorDatabase):
    def __init__(self, embedding_service):
        chroma_client = chromadb.Client(Config.CHROMA_URL)
        chroma_collection = chroma_client.create_collection("vector_store")
        
        self.vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        self.service_context = ServiceContext.from_defaults(embed_model=embedding_service)
        self.index = VectorStoreIndex.from_vector_store(self.vector_store, service_context=self.service_context)

    def insert(self, entry):
        document = entry.to_document()
        self.index.insert(document)
        return document.doc_id

    def search(self, query, entry_type, limit=10):
        query_engine = self.index.as_query_engine(similarity_top_k=limit)
        results = query_engine.query(query)
        return [entry_type.from_node(node) for node in results.source_nodes]

    def update(self, id, entry):
        self.delete(id, type(entry))
        return self.insert(entry)

    def delete(self, id, entry_type):
        self.vector_store.delete(id)