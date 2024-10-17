from rich.console import Console

from ragbits.blueprint.base import BlueprintComponentType, BlueprintComponent


class VectorStoreComponentType(BlueprintComponentType):
    name = "Vector Store"
    description = "stores embeddings and provides search functionality"


class ChromaDBComponent(BlueprintComponent):
    name = "ChromaDB"
    description = "A component for ChromaDB embeddings."
    options = {}

    @classmethod
    def help(cls):
        Console().print("""
        ChromaDB is dope.
    """)

    def generate(self):
        return """
        """


VectorStoreComponentType.register(ChromaDBComponent)
