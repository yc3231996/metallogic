from typing import List, Type
import weaviate
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.storage.storage_context import StorageContext
from config import Config
from models import BaseVectorEntry

class LlamaWeaviateDatabase:
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.client = weaviate.Client(
            url=Config.WEAVIATE_URL,
            auth_client_secret=weaviate.AuthApiKey(api_key=Config.WEAVIATE_API_KEY)
        )
        
    def _get_class_name(self, entry_type: Type[BaseVectorEntry]) -> str:
        return f"{Config.CLASS_PREFIX}{entry_type.__name__}"

    def insert(self, entry: BaseVectorEntry) -> str:
        class_name = self._get_class_name(type(entry))
        
        # Ensure the class exists
        self._create_class_if_not_exists(class_name)
        
        # Convert entry to dictionary
        entry_dict = entry.dict()
        
        # Insert the entry
        return self.client.data_object.create(
            class_name=class_name,
            data_object=entry_dict,
            vector=self.embedding_service.get_text_embedding(entry_dict["content"])
        )

    def search(self, query: str, entry_type: Type[BaseVectorEntry], limit: int = 10) -> List[BaseVectorEntry]:
        class_name = self._get_class_name(entry_type)
        
        vector = self.embedding_service.get_text_embedding(query)
        
        results = (
            self.client.query
            .get(class_name, ["content", "id"])
            .with_near_vector({
                "vector": vector,
                "certainty": 0.7
            })
            .with_limit(limit)
            .do()
        )
        
        entries = []
        for item in results["data"]["Get"][class_name]:
            entries.append(entry_type(**item))
        
        return entries

    def update(self, id: str, entry: BaseVectorEntry) -> bool:
        class_name = self._get_class_name(type(entry))
        
        entry_dict = entry.dict()
        
        self.client.data_object.update(
            class_name=class_name,
            data_object=entry_dict,
            uuid=id,
            vector=self.embedding_service.get_text_embedding(entry_dict["content"])
        )
        
        return True

    def delete(self, id: str, entry_type: Type[BaseVectorEntry]) -> bool:
        class_name = self._get_class_name(entry_type)
        
        self.client.data_object.delete(
            class_name=class_name,
            uuid=id
        )
        
        return True

    def _create_class_if_not_exists(self, class_name: str):
        if not self.client.schema.exists(class_name):
            class_obj = {
                "class": class_name,
                "vectorizer": "none"  # We're providing our own vectors
            }
            self.client.schema.create_class(class_obj)