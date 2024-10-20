import abc
from pathlib import Path
from typing import Literal

from inquirer import Path as PathType
from inquirer.shortcuts import list_input, path, text


class Option(abc.ABC):
    """
    Base class for user choices in blueprints.
    """

    @abc.abstractmethod
    def resolve(self) -> str:
        """
        Resolve the option to a value by asking the user for input.
        """


class ChoiceOption(Option):
    """
    An option that allows the user to choose from a list of options,
    wich an optional freeform option.
    """

    def __init__(self, message: str, choices: dict[str, str], allow_other: bool = False):
        self.message = message
        self.choices = choices
        self.allow_other = allow_other

    def resolve(self) -> str:
        """
        Ask user for a choice from a list of options (with an optional freeform option).

        Returns:
            The chosen option.
        """
        choices = [(desc, k) for k, desc in self.choices.items()]

        if self.allow_other:
            choices.append(("Something else... (freeform type)", "__other__"))

        chosen = list_input(self.message, choices=choices)
        if chosen == "__other__":
            return text("Enter your choice")

        return chosen


class TextOption(Option):
    """
    An option that allows the user to freeform text input.
    """

    def __init__(self, message: str, default: str | None = None):
        self.message = message
        self.default = default

    def resolve(self) -> str:
        """
        Ask user for a text input.

        Returns:
            User input.
        """
        return text(self.message, default=self.default)


class PathOption(Option):
    """
    An option that allows the user to provide filesystem path.
    """

    def __init__(
        self,
        message: str,
        default: str | None = None,
        exists: bool = False,
        absolute: bool = False,
        path_type: Literal["dir", "file"] | None = None,
    ):
        self.message = message
        self.default = default

        self.exists = exists
        self.absolute = absolute
        self.path_type = (
            PathType.DIRECTORY if path_type == "dir" else PathType.FILE if path_type == "file" else PathType.ANY
        )

    def resolve(self) -> str:
        """
        Ask user for a path input.

        Returns:
            User provided path.
        """
        result_path = path(self.message, default=self.default, exists=self.exists, path_type=self.path_type)

        return str(Path(result_path).absolute()) if self.absolute else result_path
