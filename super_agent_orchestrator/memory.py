from __future__ import annotations

from typing import Any

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from .config import MemoryConfig, ModelConfig


class LongTermMemory:
    """ChromaDB-backed long-term memory for storing and retrieving context."""

    def __init__(self, memory_config: MemoryConfig, model_config: ModelConfig) -> None:
        self.vector_store = Chroma(
            collection_name=memory_config.collection_name,
            persist_directory=memory_config.persist_directory,
            embedding_function=OpenAIEmbeddings(api_key=model_config.openai_api_key),
        )

    def remember(self, text: str, metadata: dict[str, Any] | None = None) -> None:
        doc = Document(page_content=text, metadata=metadata or {})
        self.vector_store.add_documents([doc])

    def recall(self, query: str, k: int = 4) -> list[Document]:
        return self.vector_store.similarity_search(query=query, k=k)
