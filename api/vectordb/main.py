from config import Config
from database.llama_weaviate import LlamaWeaviateDatabase
from database.llama_chroma import LlamaChromaDatabase
from embedding import get_embedding_service
from models import QuestionAnswer, TermDescription, VisualizationInstruction

class VectorDatabaseSystem:
    def __init__(self):
        self.embedding_service = get_embedding_service(Config.EMBEDDING_SERVICE)
        if Config.VECTOR_DB == "weaviate":
            self.db = LlamaWeaviateDatabase(self.embedding_service)
        elif Config.VECTOR_DB == "chroma":
            self.db = LlamaChromaDatabase(self.embedding_service)
        else:
            raise ValueError(f"Unsupported vector database: {Config.VECTOR_DB}")

    def insert_question_answer(self, question, answer):
        entry = QuestionAnswer(id="", question=question, answer=answer)
        return self.db.insert(entry)

    def insert_term_description(self, term, description):
        entry = TermDescription(id="", term=term, description=description)
        return self.db.insert(entry)

    def insert_visualization_instruction(self, instruction, chart_config):
        entry = VisualizationInstruction(id="", instruction=instruction, chart_config=chart_config)
        return self.db.insert(entry)

    def search_question_answers(self, query, limit=10):
        return self.db.search(query, QuestionAnswer, limit)

    def search_term_descriptions(self, query, limit=10):
        return self.db.search(query, TermDescription, limit)

    def search_visualization_instructions(self, query, limit=10):
        return self.db.search(query, VisualizationInstruction, limit)

    def update_entry(self, id, entry):
        return self.db.update(id, entry)

    def delete_entry(self, id, entry_type):
        return self.db.delete(id, entry_type)

# Usage example
if __name__ == "__main__":
    system = VectorDatabaseSystem()

    # Insert examples
    qa_id = system.insert_question_answer("What is the capital of France?", "The capital of France is Paris.")
    term_id = system.insert_term_description("Python", "Python is a high-level, interpreted programming language.")
    vis_id = system.insert_visualization_instruction("Create a bar chart of sales by month", {"type": "bar", "data": {...}})

    # Search examples
    qa_results = system.search_question_answers("capital of France")
    term_results = system.search_term_descriptions("programming language")
    vis_results = system.search_visualization_instructions("bar chart")

    # Update example
    updated_qa = QuestionAnswer(id=qa_id, question="What is the capital of France?", answer="The capital of France is Paris, also known as the City of Light.")
    system.update_entry(qa_id, updated_qa)

    # Delete example
    system.delete_entry(term_id, TermDescription)