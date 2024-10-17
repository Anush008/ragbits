import textwrap

from rich.console import Console

from ragbits.blueprint.base import BlueprintComponentType, BlueprintComponent
from ragbits.blueprint.options import ChoiceOption


class LLMComponentType(BlueprintComponentType):
    name = "LLM Provider"
    description = "will be used for text generation or reasoning tasks"


class LiteLLMComponent(BlueprintComponent):
    name = "LiteLLM"
    description = "supports more than 100 LLM providers with unified API."
    options = {
        "model_name": ChoiceOption(
            message="Choose a model",
            choices={
                "gpt4o": "OpenAI gpt-4o",
                "gpt4": "OpenAI gpt-4",
                "gpt3": "OpenAI gpt-3",
                "gemini": "Google Gemini"
            },
            allow_other=True,
        )
    }

    @classmethod
    def help(cls):
        Console().print(
            "LiteLLM supports more than 100 Large Language Models providers with unified API.\n"
            "For more information, visit https://docs.litellm.ai/"
        )

    def generate(self) -> str:
        return textwrap.dedent(f"""
        from ragbits.core.llms import LiteLLM",

        def get_llm():
            return LiteLLM(model_name="{self._selected_options["model_name"]}")
        """)




LLMComponentType.clear()
LLMComponentType.register(LiteLLMComponent)

