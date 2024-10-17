import textwrap

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

    def generate(self) -> str:
        """
        Create a string with the code for the blueprint.

        Returns:
            A string with the code for the blueprint.
        """
        imports = self.generate_imports()
        components = self.generate_components()

        imports = (
            "import asyncio\n"
            + imports
            + "\n"
            + textwrap.dedent(
                """
            from pydantic import BaseModel
            from ragbits.core.prompt import Prompt
            from ragbits.document_search.documents.element import Element
            """
            ).strip()
        )

        body = (
            components
            + "\n\n"
            + textwrap.dedent(
                '''
            class QAInput(BaseModel):
                elements: list[Element]
                question: str


            class QAPrompt(Prompt[QAInput, str]):

                system_prompt = """
                Your task is to answer user question based on the context provided in the document.

                <context>
                    {% for element in elements %}
                        {{ element.content }}
                    {% endfor %}
                </context>
                """

                user_prompt = """{question}"""

            async def answer(question: str):
                llm = get_llm()
                document_search = get_document_search()

                elements = await document_search.search(question)

                response = await llm.generate(QAPrompt(QAInput(question=question, elements=elements)))
                return response, elements


            async def ingest(documents):
                document_search = get_document_search()
                await document_search.ingest(documents)


            if __name__ == '__main__':
                asyncio.run(answer("my_question"))
            '''
            ).strip()
        )
        return f"{imports}\n\n{body}\n"
