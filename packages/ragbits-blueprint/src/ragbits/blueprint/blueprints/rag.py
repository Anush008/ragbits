from typing import Annotated

from ragbits.blueprint.base import Blueprint
from ragbits.blueprint.components.embeddings import EmbeddingsComponentType
from ragbits.blueprint.components.llm import LLMComponentType
from ragbits.blueprint.components.vector_store import VectorStoreComponentType


class RAGBlueprint(Blueprint):
    name = "RAG Chatbot"
    description = "A blueprint for RAG applications."
    components = [
        LLMComponentType,
        EmbeddingsComponentType,
        VectorStoreComponentType
    ]

    @classmethod
    def help(cls):
        print()

    def generate(self):
        print("---")
        print("src/app/components.py")

        print(self._selected_components[LLMComponentType].generate())
        print(self._selected_components[EmbeddingsComponentType].generate())
        print(self._selected_components[VectorStoreComponentType].generate())