# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "ragbits-document-search",
#     "ragbits-core[chroma,litellm]",
# ]
# ///
import asyncio

from ragbits.document_search import DocumentSearch
from ragbits.document_search.documents.document import DocumentMeta

documents = [
    DocumentMeta.create_text_document_from_literal("RIP boiled water. You will be mist."),
    DocumentMeta.create_text_document_from_literal(
        "Why doesn't James Bond fart in bed? Because it would blow his cover."
    ),
    DocumentMeta.create_text_document_from_literal(
        "Why programmers don't like to swim? Because they're scared of the floating points."
    ),
]

config = {
    "embedder": {"type": "ragbits.core.embeddings.litellm:LiteLLMEmbeddings"},
    "vector_store": {
        "type": "ragbits.core.vector_stores.chroma:ChromaVectorStore",
        "config": {
            "client": {
                "type": "PersistentClient",
                "config": {
                    "path": "chroma",
                },
            },
            "index_name": "jokes",
            "distance_method": "l2",
            "default_options": {
                "k": 3,
                "max_distance": 1.2,
            },
            "metadata_store": {
                "type": "InMemoryMetadataStore",
            },
        },
    },
    "reranker": {"type": "ragbits.document_search.retrieval.rerankers.noop:NoopReranker"},
    "providers": {"txt": {"type": "DummyProvider"}},
    "rephraser": {
        "type": "LLMQueryRephraser",
        "config": {
            "llm": {
                "type": "ragbits.core.llms.litellm:LiteLLM",
                "config": {
                    "model_name": "gpt-4-turbo",
                },
            },
            "prompt": "QueryRephraserPrompt",
        },
    },
}


async def main() -> None:
    """
    Run the example.
    """
    document_search = DocumentSearch.from_config(config)

    await document_search.ingest(documents)

    results = await document_search.search("I'm boiling my water and I need a joke")
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
