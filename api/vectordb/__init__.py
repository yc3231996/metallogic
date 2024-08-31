from .config import Config
from .models import VectorEntry, QuestionAnswer, TermDescription, VisualizationInstruction
from .database import VectorDatabase, LlamaWeaviateDatabase, LlamaChromaDatabase
from .embedding import EmbeddingService, OpenAIEmbedding
from .main import VectorDatabaseSystem

__all__ = [
    'Config',
    'VectorEntry', 'QuestionAnswer', 'TermDescription', 'VisualizationInstruction',
    'VectorDatabase', 'LlamaWeaviateDatabase', 'LlamaChromaDatabase',
    'EmbeddingService', 'OpenAIEmbedding',
    'VectorDatabaseSystem'
]

__version__ = "0.1.0"
__author__ = "Your Name"
__description__ = "A flexible vector database system supporting multiple backends."