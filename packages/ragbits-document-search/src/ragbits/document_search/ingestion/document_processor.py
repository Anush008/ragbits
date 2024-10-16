import copy

from ragbits.document_search.documents.document import DocumentMeta, DocumentType
from ragbits.document_search.ingestion.providers import get_provider
from ragbits.document_search.ingestion.providers.base import BaseProvider
from ragbits.document_search.ingestion.providers.unstructured import (
    UnstructuredProvider,
)

ProvidersConfig = dict[DocumentType, BaseProvider]


DEFAULT_PROVIDERS_CONFIG: ProvidersConfig = {
    DocumentType.TXT: UnstructuredProvider(),
    DocumentType.MD: UnstructuredProvider(),
    DocumentType.PDF: UnstructuredProvider(),
    DocumentType.DOCX: UnstructuredProvider(),
    DocumentType.DOC: UnstructuredProvider(),
    DocumentType.PPTX: UnstructuredProvider(),
    DocumentType.PPT: UnstructuredProvider(),
    DocumentType.XLSX: UnstructuredProvider(),
    DocumentType.XLS: UnstructuredProvider(),
    DocumentType.CSV: UnstructuredProvider(),
    DocumentType.HTML: UnstructuredProvider(),
    DocumentType.EPUB: UnstructuredProvider(),
    DocumentType.ORG: UnstructuredProvider(),
    DocumentType.ODT: UnstructuredProvider(),
    DocumentType.RST: UnstructuredProvider(),
    DocumentType.RTF: UnstructuredProvider(),
    DocumentType.TSV: UnstructuredProvider(),
    DocumentType.XML: UnstructuredProvider(),
}


class DocumentProcessorRouter:
    """
    The DocumentProcessorRouter is responsible for routing the document to the correct provider based on the document
    metadata such as the document type.
    """

    def __init__(self, providers: dict[DocumentType, BaseProvider]):
        self._providers = providers

    @staticmethod
    def from_dict_to_providers_config(dict_config: dict) -> ProvidersConfig:
        """
        Creates ProvidersConfig from dictionary config.
        Example of the dictionary config:
        {
            "txt": {
                {
                    "type": "UnstructuredProvider"
                }
            }
        }

        Args:
            dict_config: The dictionary with configuration.

        Returns:
            ProvidersConfig object.
        """
        providers_config = {}

        for document_type, config in dict_config.items():
            providers_config[DocumentType(document_type)] = get_provider(config)

        return providers_config

    @classmethod
    def from_config(cls, providers_config: ProvidersConfig | None = None) -> "DocumentProcessorRouter":
        """
        Create a DocumentProcessorRouter from a configuration. If the configuration is not provided, the default
        configuration will be used. If the configuration is provided, it will be merged with the default configuration,
        overriding the default values for the document types that are defined in the configuration.
        Example of the configuration:
        {
            DocumentType.TXT: YourCustomProviderClass(),
            DocumentType.PDF: UnstructuredProvider(),
        }

        Args:
            providers_config: The dictionary with the providers configuration, mapping the document types to the
             provider class.

        Returns:
            The DocumentProcessorRouter.
        """
        config = copy.deepcopy(DEFAULT_PROVIDERS_CONFIG)
        config.update(providers_config if providers_config is not None else {})

        return cls(providers=config)

    def get_provider(self, document_meta: DocumentMeta) -> BaseProvider:
        """
        Get the provider for the document.

        Args:
            document_meta: The document metadata.

        Returns:
            The provider for processing the document.

        Raises:
            ValueError: If no provider is found for the document type.
        """
        provider = self._providers.get(document_meta.document_type)
        if provider is None:
            raise ValueError(f"No provider found for the document type {document_meta.document_type}")
        return provider
