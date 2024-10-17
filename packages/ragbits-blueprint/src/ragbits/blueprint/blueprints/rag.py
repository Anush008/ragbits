from ragbits.blueprint.base import Blueprint
from ragbits.blueprint.components.embeddings import EmbeddingsComponentType
from ragbits.blueprint.components.llm import LLMComponentType
from ragbits.blueprint.components.vector_store import VectorStoreComponentType


class RAGBlueprint(Blueprint):
    """
    A blueprint for RAG applications.
    """

    name = "RAG Chatbot"
    description = "A blueprint for RAG applications."
    components = [LLMComponentType, EmbeddingsComponentType, VectorStoreComponentType]

    @classmethod
    def help(cls) -> str:
        """
        Get a help message for the blueprint.

        Returns:
            A help message for the blueprint.
        """
        return "Generates a RAG chatbot application with LLM, Embeddings, and Vector Store."
