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

    def generate(self) -> str:
        """
        Generate the code for the component.

        Returns:
            The code for the component.
        """
        return "ChromaDB()"


VectorStoreComponentType.register(ChromaDBComponent)
