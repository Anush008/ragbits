import abc
from typing import Generic, TypeVar

from inquirer.shortcuts import list_input, text

T = TypeVar("T")


class Option(Generic[T], abc.ABC):

    @abc.abstractmethod
    def resolve(self) -> T:
        pass


class ChoiceOption(Option[T]):
    def __init__(self, message: str, choices: dict[T, str], allow_other: bool = False):
        self.message = message
        self.choices = choices
        self.allow_other = allow_other

    def resolve(self) -> str:
        choices = [(desc, k) for k, desc in self.choices.items()]

        if self.allow_other:
            choices.append(("Something else... (freeform type)", "__other__"))

        chosen = list_input(self.message, choices=[choice for choice in choices])
        if chosen == "__other__":
            return text("Enter your choice")

        return chosen