from rich.console import Console

from ragbits.blueprint.base import BlueprintComponentType, BlueprintComponent
from ragbits.blueprint.options import ChoiceOption


class EmbeddingsComponentType(BlueprintComponentType):
    name = "Embeddings Provider"
    description = "will be used to create vector representations of elements and for search functionality"


class LiteLLMEmbeddingsComponent(BlueprintComponent):
    name = "LiteLLM Embeddings"
    description = "supports most popular embeddings providers with unified API."
    options = {
        "model_name": ChoiceOption(
            message="Choose a model",
            choices={
                "text-embedding-3-small": "OpenAI text-embedding-4-small",
                "text-embedding-3-large": "OpenAI text-embedding-4-large",
            },
            allow_other=True,
        )
    }

    @classmethod
    def help(cls):
        Console().print(
            "For more information, visit https://docs.litellm.ai/"
        )

    def generate(self):
        return {
            "model_name": self.options["model_name"]
        }


EmbeddingsComponentType.register(LiteLLMEmbeddingsComponent)
