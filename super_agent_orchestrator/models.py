from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from .config import ModelConfig


class ModelRegistry:
    """Factory and registry for specialist LLMs."""

    def __init__(self, config: ModelConfig) -> None:
        self.config = config

    def build_openai_generalist(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.config.openai_model,
            api_key=self.config.openai_api_key,
            temperature=0.2,
        )

    def build_openai_logic_specialist(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.config.openai_logic_model,
            api_key=self.config.openai_api_key,
            temperature=0,
        )

    def build_gemini_analyst(self) -> BaseChatModel:
        return ChatGoogleGenerativeAI(
            model=self.config.gemini_model,
            google_api_key=self.config.google_api_key,
            temperature=0.2,
        )

    def build_grok_realtime(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.config.grok_model,
            api_key=self.config.grok_api_key,
            base_url="https://api.x.ai/v1",
            temperature=0.3,
        )

    def build_specialists(self) -> dict[str, BaseChatModel]:
        return {
            "openai_general": self.build_openai_generalist(),
            "openai_logic": self.build_openai_logic_specialist(),
            "gemini_analyst": self.build_gemini_analyst(),
            "grok_realtime": self.build_grok_realtime(),
        }
