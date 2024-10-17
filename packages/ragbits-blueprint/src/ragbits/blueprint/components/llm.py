import textwrap

from ragbits.blueprint.base import BlueprintComponent, BlueprintComponentType
from ragbits.blueprint.options import ChoiceOption


class LLMComponentType(BlueprintComponentType):
    """
    A component type for LLM providers.
    """

    name = "LLM Provider"
    description = "will be used for text generation or reasoning tasks"


class LiteLLMComponent(BlueprintComponent):
    """
    LiteLLM component for LLM providers.
    """

    name = "LiteLLM"
    description = "supports more than 100 LLM providers with unified API."
    options = {
        "model_name": ChoiceOption(
            message="Choose a model",
            choices={
                "gpt4o": "OpenAI gpt-4o",
                "gpt4": "OpenAI gpt-4",
                "gpt3": "OpenAI gpt-3",
                "gemini": "Google Gemini",
            },
            allow_other=True,
        )
    }

    @classmethod
    def help(cls) -> str:
        """
        Get a help message for the component.

        Returns:
            A help message for the component.
        """
        return (
            "LiteLLM supports more than 100 Large Language Models providers with unified API.\n"
            "For more information, visit https://docs.litellm.ai/"
        )

    def generate_imports(self) -> list[str]:
        """
        Generate the imports for the component.

        Returns:
            A list of strings with the imports.
        """
        return ["from ragbits.core.llms import LiteLLM"]

    def generate(self) -> str:
        """
        Generate the code for the component.

        Returns:
            The code for the component.
        """
        return textwrap.dedent(
            f"""
        def get_llm():
            return LiteLLM(model_name="{self._selected_options["model_name"]}")
        """
        ).strip()


LLMComponentType.clear()
LLMComponentType.register(LiteLLMComponent)
