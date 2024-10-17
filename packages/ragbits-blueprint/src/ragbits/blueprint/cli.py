import typer
from inquirer.shortcuts import list_input

from ragbits.blueprint.blueprints import BLUEPRINTS


def register(app: typer.Typer, help_only: bool) -> None:  # pylint: disable=unused-argument
    """
    Register the CLI commands for the package.

    Args:
        app: The Typer object to register the commands with.
        help_only: Whether to only register the help command.
    """

    @app.command()
    def blueprint() -> None:
        """
        Generate a blueprint for a project interactively.
        """
        blueprint = list_input("Which blueprint", choices=[(f"{bp.name}: {bp.description}", bp) for bp in BLUEPRINTS])
        blueprint.help()
        build = blueprint.collect()
        print(build.generate())
