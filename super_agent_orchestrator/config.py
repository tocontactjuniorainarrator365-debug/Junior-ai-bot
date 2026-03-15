from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    """Configuration for model and API credentials."""

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    grok_api_key: str | None = os.getenv("GROK_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    openai_logic_model: str = os.getenv("OPENAI_LOGIC_MODEL", "gpt-5")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    grok_model: str = os.getenv("GROK_MODEL", "grok-beta")


@dataclass(frozen=True)
class SearchConfig:
    """Google search configuration via Custom Search API."""

    google_cse_api_key: str | None = os.getenv("GOOGLE_CSE_API_KEY")
    google_cse_id: str | None = os.getenv("GOOGLE_CSE_ID")


@dataclass(frozen=True)
class GitHubConfig:
    """GitHub API configuration."""

    github_token: str | None = os.getenv("GITHUB_TOKEN")
    github_repo: str | None = os.getenv("GITHUB_REPO")


@dataclass(frozen=True)
class MemoryConfig:
    """Long-term memory storage settings."""

    collection_name: str = os.getenv("CHROMA_COLLECTION", "super_agent_memory")
    persist_directory: str = os.getenv("CHROMA_DIR", "./.chroma")
