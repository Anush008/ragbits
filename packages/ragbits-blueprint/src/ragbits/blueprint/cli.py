import typer
from inquirer.shortcuts import confirm, list_input

from ragbits.blueprint.blueprints import BLUEPRINTS


def register(app: typer.Typer, help_only) -> None:
    """
    Register the CLI commands for the package.

    Args:
        app: The Typer object to register the commands with.
    """


    @app.command()
    def blueprint():
        blueprint = list_input(
            "Which blueprint",
            choices=[
                (f"{bp.name}: {bp.description}", bp)
                for bp in BLUEPRINTS
            ]
        )
        blueprint.help()
        build = blueprint.collect()
        build.generate()