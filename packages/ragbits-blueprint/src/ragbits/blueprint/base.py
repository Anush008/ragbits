from abc import ABC, abstractmethod
from typing import ClassVar, Any

from inquirer import list_input
from rich.console import Console
from typing_extensions import Self

from ragbits.blueprint.options import Option


class BlueprintComponent(ABC):
    name: ClassVar[str]
    description: ClassVar[str]
    options: ClassVar[dict[str, Option]] = {}

    _selected_options: dict[str, Any]

    def __init__(self, selected_options):
        self._selected_options = selected_options

    @classmethod
    def info(cls):
        return f"{cls.name}: {cls.description}"

    @classmethod
    def help(cls):
        pass

    @classmethod
    def collect(cls) -> Self:
        Console().print(f"Configuring [cyan bold]{cls.name}...\n")
        cls.help()
        Console().print("\n")
        collected = {}
        for option_name, option in cls.options.items():
            collected[option_name] = option.resolve()
        return cls(collected)

    @abstractmethod
    def generate(self) -> str:
        pass


class BlueprintComponentType(ABC):

    name: ClassVar[str]
    description: ClassVar[str]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._components = set()

    @classmethod
    def register(cls, component: type[BlueprintComponent]):
        cls._components.add(component)

    @classmethod
    def clear(cls):
        cls._components.clear()

    @classmethod
    def remove(cls, component: type[BlueprintComponent]):
        cls._components.remove(component)

    @classmethod
    def get_components(cls) -> list[type[BlueprintComponent]]:
        return list(cls._components)

    @classmethod
    def info(cls):
        return f"{cls.name}: {cls.description}"


class Blueprint(ABC):
    name: ClassVar[str]
    description: ClassVar[str]

    options: dict[str, str] = {}
    components: ClassVar[list[type[BlueprintComponentType]]]

    _selected_options: dict[str, str]
    _selected_components: dict[type[BlueprintComponentType], BlueprintComponent]

    def __init__(self, selected_options: dict[str, str], selected_components: dict[type[BlueprintComponentType], BlueprintComponent]):
        self._selected_options = selected_options
        self._selected_components = selected_components

    @classmethod
    def collect(cls) -> Self:
        _selected_components = {}
        for component_type in cls.components:
            components = component_type.get_components()
            chosen = list_input(
                message=f"Choose {component_type.info()}",
                choices=[(component.info(), component) for component in components]
            )

            _selected_components[component_type] = chosen.collect()

        return cls({}, _selected_components)

    @classmethod
    def help(cls):
        pass

    def build(self):
        pass

