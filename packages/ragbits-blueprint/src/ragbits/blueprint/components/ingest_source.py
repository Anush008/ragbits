import textwrap

from ragbits.blueprint.base import BlueprintComponent, BlueprintComponentType
from ragbits.blueprint.options import PathOption, TextOption


class IngestionSourceComponentType(BlueprintComponentType):
    """
    A component type for ingesting documents into document search.
    """

    name = "Ingestion Source"
    description = "select the source of the data to be ingested."


class LocalIngestionSourceComponent(BlueprintComponent):
    """
    Local ingestion source component.
    """

    name = "Local filesystem"
    description = "select documents that are stored locally (not recommended for prod)."
    options = {
        "path": PathOption(
            message="Path to the directory containing documents", exists=True, path_type="dir", absolute=True
        ),
        "pattern": TextOption(message="Pattern to match files in the directory", default="*/**"),
    }

    @classmethod
    def help(cls) -> str:
        """
        Get a help message for the component.

        Returns:
            A help message for the component.
        """
        return ""

    def generate_imports(self) -> list[str]:
        """
        Generate the imports for the component.

        Returns:
            A list of strings with the imports.
        """
        return ["from ragbits.document_search.documents.sources import LocalFileSource"]

    def generate(self) -> str:
        """
        Generate the code for the component.

        Returns:
            The code for the component.
        """
        return (
            f'LocalFileSource.list_sources(path="{self._selected_options["path"]}", '
            f'file_pattern="{self._selected_options["pattern"]}")'
        )


IngestionSourceComponentType.register(LocalIngestionSourceComponent)


class GCSIngestionSourceComponent(BlueprintComponent):
    """
    GCS ingestion source component.
    """

    name = "Google Cloud Storage"
    description = "fetch documents from Google Cloud Storage bucket."
    options = {
        "bucket": TextOption(message="Bucket in which the documents are stored"),
        "prefix": TextOption(
            message="From what prefix download the documents (leave blank for whole bucket)", default=""
        ),
    }

    @classmethod
    def help(cls) -> str:
        """
        Get a help message for the component.

        Returns:
            A help message for the component.
        """
        return textwrap.dedent(
            """
            Make sure that you have configured the GCS [b]application default credentials (ADC)[/b].
            For more info visit https://cloud.google.com/docs/authentication/getting-started
        """
        )

    def generate_imports(self) -> list[str]:
        """
        Generate the imports for the component.

        Returns:
            A list of strings with the imports.
        """
        return ["from ragbits.document_search.documents.sources import GCSSource"]

    def generate(self) -> str:
        """
        Generate the code for the component.

        Returns:
            The code for the component.
        """
        return (
            f'GCSSource.list_sources(bucket="{self._selected_options["bucket"]}", '
            f'prefix="{self._selected_options["prefix"]}")'
        )


IngestionSourceComponentType.register(GCSIngestionSourceComponent)
