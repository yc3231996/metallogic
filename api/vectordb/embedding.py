from abc import ABC, abstractmethod
from llama_index import OpenAIEmbedding, HuggingFaceEmbedding

class BaseEmbeddingService(ABC):
    @abstractmethod
    def get_text_embedding(self, text: str) -> list[float]:
        pass

class OpenAIEmbeddingService(BaseEmbeddingService):
    def __init__(self):
        self.embed_model = OpenAIEmbedding()

    def get_text_embedding(self, text: str) -> list[float]:
        return self.embed_model.get_text_embedding(text)

class HuggingFaceEmbeddingService(BaseEmbeddingService):
    def __init__(self, model_name: str):
        self.embed_model = HuggingFaceEmbedding(model_name=model_name)

    def get_text_embedding(self, text: str) -> list[float]:
        return self.embed_model.get_text_embedding(text)

def get_embedding_service(service_name: str, **kwargs) -> BaseEmbeddingService:
    if service_name.lower() == "openai":
        return OpenAIEmbeddingService()
    elif service_name.lower() == "huggingface":
        model_name = kwargs.get("model_name", "sentence-transformers/all-MiniLM-L6-v2")
        return HuggingFaceEmbeddingService(model_name)
    else:
        raise ValueError(f"Unsupported embedding service: {service_name}")