from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Complexity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class RouteDecision:
    specialist_key: str
    complexity: Complexity
    reason: str


class MultiModelRouter:
    """Routes tasks to OpenAI GPT-7, Gemini 5.3, or Grok specialists."""

    REALTIME_HINTS = {
        "latest",
        "real-time",
        "current",
        "news",
        "today",
        "now",
        "live",
        "breaking",
        "trend",
    }
    HIGH_COMPLEXITY_HINTS = {
        "prove",
        "formal",
        "architecture",
        "multi-step",
        "algorithm",
        "optimize",
        "trade-off",
        "deep reasoning",
    }

    def classify_complexity(self, task: str) -> Complexity:
        normalized = task.lower()
        token_count = len(normalized.split())

        if token_count > 70 or any(hint in normalized for hint in self.HIGH_COMPLEXITY_HINTS):
            return Complexity.HIGH
        if token_count > 25:
            return Complexity.MEDIUM
        return Complexity.LOW

    def choose_specialist(self, task: str) -> RouteDecision:
        normalized = task.lower()
        complexity = self.classify_complexity(task)

        if any(hint in normalized for hint in self.REALTIME_HINTS):
            return RouteDecision(
                specialist_key="grok_realtime",
                complexity=complexity,
                reason="Task asks for up-to-date or real-time information, routed to Grok.",
            )

        if complexity is Complexity.HIGH:
            return RouteDecision(
                specialist_key="openai_logic",
                complexity=complexity,
                reason="High-complexity logic task routed to GPT-7 logic specialist.",
            )

        return RouteDecision(
            specialist_key="gemini_understanding",
            complexity=complexity,
            reason="Low/medium complexity understanding task routed to Gemini 5.3.",
        )
