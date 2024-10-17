import abc

from inquirer.shortcuts import list_input, text


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
