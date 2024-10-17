from abc import ABC, abstractmethod
from typing import Any, ClassVar

from inquirer import list_input
from rich.console import Console
from typing_extensions import Self

from ragbits.blueprint.options import Option


class BlueprintComponent(ABC):
    """
    Base class for components that can be added to a blueprint.
    """

    name: ClassVar[str]
    description: ClassVar[str]
    options: ClassVar[dict[str, Option]] = {}

    _selected_options: dict[str, Any]

    def __init__(self, selected_options: dict[str, Any]):
        self._selected_options = selected_options

    @classmethod
    def info(cls) -> str:
        """
        Get a string with information about the component.

        Returns:
            A string with the component name and description.
        """
        return f"{cls.name}: {cls.description}"

    @classmethod
    def help(cls) -> str:
        """
        Return help information about the component.

        Returns:
            A help string.
        """
        return ""

    @classmethod
    def collect(cls) -> Self:
        """
        Collect the options for the component interactively.

        Returns:
            An instance of the component with the selected options.
        """
        Console().print(f"Configuring [cyan bold]{cls.name}...\n")
        Console().print(cls.help())
        Console().print("\n")
        collected = {}
        for option_name, option in cls.options.items():
            collected[option_name] = option.resolve()
        return cls(collected)

    def generate_imports(self) -> list[str]:
        """
        Generate a list of imports (lines that should be added to the top of the file)
        needed for this component.

        Returns:
            List of import strings.
        """
        return []

    @abstractmethod
    def generate(self) -> str:
        """
        Generate the code for the component in the blueprint.
        """


class BlueprintComponentType(ABC):
    """
    Base class for types of components that can be added to a blueprint.

    Each component type can have multiple components, which can be registered
    with the type.
    """

    name: ClassVar[str]
    description: ClassVar[str]
    _components: set[type[BlueprintComponent]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Initialize the subclass by setting by setting up its indyvidual component set.

        Args:
            **kwargs: Keyword arguments.
        """
        super().__init_subclass__(**kwargs)
        cls._components = set()

    @classmethod
    def register(cls, component: type[BlueprintComponent]) -> None:
        """
        Register a component with the component type.

        Args:
            component: The component class to register.
        """
        cls._components.add(component)

    @classmethod
    def clear(cls) -> None:
        """
        Clear the list of registered components.
        """
        cls._components.clear()

    @classmethod
    def remove(cls, component: type[BlueprintComponent]) -> None:
        """
        Remove a component from the list of registered components.

        Args:
            component: The component class to remove.
        """
        cls._components.remove(component)

    @classmethod
    def get_components(cls) -> list[type[BlueprintComponent]]:
        """
        Get a list of registered components.

        Returns:
            A list of registered components.
        """
        return list(cls._components)

    @classmethod
    def info(cls) -> str:
        """
        Get a string with information about the component type.

        Returns:
            A string with the component type name and description.
        """
        return f"{cls.name}: {cls.description}"


class Blueprint(ABC):
    """
    Base class for blueprints that can be generated interactively.
    """

    name: ClassVar[str]
    description: ClassVar[str]

    options: dict[str, str] = {}
    components: ClassVar[list[type[BlueprintComponentType]]]

    _selected_options: dict[str, str]
    _selected_components: dict[type[BlueprintComponentType], BlueprintComponent]

    def __init__(
        self,
        selected_options: dict[str, str],
        selected_components: dict[type[BlueprintComponentType], BlueprintComponent],
    ):
        self._selected_options = selected_options
        self._selected_components = selected_components

    @classmethod
    def collect(cls) -> Self:
        """
        Collect all components (and their options) for the blueprint interactively.

        Returns:
            An instance of the blueprint with the selected components and options.
        """
        _selected_components = {}
        for component_type in cls.components:
            components = component_type.get_components()
            chosen = list_input(
                message=f"Choose {component_type.info()}",
                choices=[(component.info(), component) for component in components],
            )

            _selected_components[component_type] = chosen.collect()

        return cls({}, _selected_components)

    @classmethod
    def help(cls) -> str:
        """
        Return help information about the blueprint.

        Returns:
            A help string.
        """
        return ""

    def generate_imports(self) -> str:
        """
        Generate a string with the imports needed by the chosen components.

        Returns:
            A string with the imports.
        """
        imports = []
        for component in self._selected_components.values():
            imports.extend(component.generate_imports())
        return "\n".join(imports)

    def generate_components(self) -> str:
        """
        Generate a string with the code for the chosen components.

        Returns:
            A string with the code for the components.
        """
        code = []
        for component in self._selected_components.values():
            code.append(component.generate())
        return "\n\n".join(code)

    def generate(self) -> str:
        """
        Create a string with the code for the blueprint.

        Returns:
            A string with the code for the blueprint.
        """
        imports = self.generate_imports()
        components = self.generate_components()
        return f"{imports}\n\n{components}"
