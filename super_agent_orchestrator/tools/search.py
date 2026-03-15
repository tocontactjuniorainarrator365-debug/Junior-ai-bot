from __future__ import annotations

import requests
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from ..config import SearchConfig


class GoogleSearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    num_results: int = Field(default=5, description="Maximum number of results")


class GoogleSearchTool(BaseTool):
    name: str = "google_search"
    description: str = "Search the web using Google Custom Search API."
    args_schema: type[BaseModel] = GoogleSearchInput
    config: SearchConfig

    def _run(self, query: str, num_results: int = 5) -> str:
        if not self.config.google_cse_api_key or not self.config.google_cse_id:
            return "Google Search is not configured. Set GOOGLE_CSE_API_KEY and GOOGLE_CSE_ID."

        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": self.config.google_cse_api_key,
                "cx": self.config.google_cse_id,
                "q": query,
                "num": num_results,
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        items = payload.get("items", [])

        if not items:
            return "No results found."

        lines = []
        for idx, item in enumerate(items, start=1):
            lines.append(f"{idx}. {item.get('title')}\n{item.get('link')}\n{item.get('snippet')}")
        return "\n\n".join(lines)
