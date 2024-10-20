import typer
from inquirer.shortcuts import list_input
from rich import print as rprint
from rich.syntax import Syntax

from ragbits.blueprint.blueprints import BLUEPRINTS


def register(app: typer.Typer) -> None:  # pylint: disable=unused-argument
    """
    Register the CLI commands for the package.

    Args:
        app: The Typer object to register the commands with.
        help_only: Whether to only register the help command.
    """

    def write_to_file(content: str, path: str) -> None:
        """
        Write content to a file.

        Args:
            content: The content to write.
            path: The file to write the content to.
        """
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    @app.command()
    # pylint: disable=missing-param-doc
    def blueprint(output: str | None = typer.Option(default=None, help="Output file for the blueprint")) -> None:
        """
        Generate a blueprint for a project interactively.
        """
        chosen_bp = list_input("Which blueprint", choices=[(f"{bp.name}: {bp.description}", bp) for bp in BLUEPRINTS])
        rprint(chosen_bp.help())
        build = chosen_bp.collect()

        if output:
            write_to_file(build.generate(), output)
            rprint(f"Blueprint written to [bold]{output}[/bold]")
        else:
            rprint("[b]Blueprint generated:[/b]")
            rprint()

            generated = build.generate()
            rprint(Syntax(generated, "python", theme="monokai", line_numbers=False))
            rprint()
