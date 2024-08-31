from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from llama_index.schema import Document

@dataclass
class VectorEntry:
    id: str

    @classmethod
    def vector_field(cls):
        raise NotImplementedError

    def to_dict(self):
        return asdict(self)

    def to_document(self):
        return Document(
            text=getattr(self, self.vector_field()),
            metadata=self.to_dict()
        )

    @classmethod
    def from_node(cls, node):
        return cls(**node.metadata)

@dataclass
class QuestionAnswer(VectorEntry):
    question: str
    answer: str

    @classmethod
    def vector_field(cls):
        return "question"

@dataclass
class TermDescription(VectorEntry):
    term: str
    description: str

    @classmethod
    def vector_field(cls):
        return "term"

@dataclass
class VisualizationInstruction(VectorEntry):
    instruction: str
    chart_config: Dict[str, Any]

    @classmethod
    def vector_field(cls):
        return "instruction"
    