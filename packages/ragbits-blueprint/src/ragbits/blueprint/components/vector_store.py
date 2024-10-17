import textwrap

from ragbits.blueprint.base import BlueprintComponent, BlueprintComponentType


class VectorStoreComponentType(BlueprintComponentType):
    """
    A component type for vector stores.
    """

    name = "Vector Store"
    description = "stores embeddings and provides search functionality"


class ChromaDBComponent(BlueprintComponent):
    """
    ChromaDB vector store component.
    """

    name = "ChromaDB"
    description = "A component for ChromaDB embeddings."
    options = {}

    @classmethod
    def help(cls) -> str:
        """
        Get a help message for the component.

        Returns:
            A help message for the component.
        """
        return "For more information, visit https://trychroma.com/"

    def generate_imports(self) -> list[str]:
        """
        Generate the imports for the component.

        Returns:
            A list of strings with the imports.
        """
        return [
            "import chromadb",
            "from ragbits.document_search import DocumentSearch",
            "from ragbits.core.vector_store import ChromaDBStore",
        ]

    def generate(self) -> str:
        """
        Generate the code for the component.

        Returns:
            The code for the component.
        """
        return textwrap.dedent(
            """
            def get_document_search():
                embeddings = get_embeddings()
                chroma_client = chromadb.PersistentClient(path="/tmp/chromadb_sample_rag")
                return DocumentSearch(
                    embedder=embeddings,
                    vector_store=ChromaDBStore(
                        index_name="sample-rag",
                        embedding_function=embeddings,
                        chroma_client=chroma_client
                    ),
                )
            """
        ).strip()


VectorStoreComponentType.register(ChromaDBComponent)
