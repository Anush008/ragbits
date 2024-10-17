from ragbits.blueprint.base import Blueprint
from ragbits.blueprint.components.llm import LLMComponentType


class BasicBlueprint(Blueprint):
    """
    A basic blueprint for ragbits applications with just the LLM component.
    """

    name = "Basic Blueprint"
    description = "A basic blueprint for ragbits applications."
    components = [
        LLMComponentType,
    ]
