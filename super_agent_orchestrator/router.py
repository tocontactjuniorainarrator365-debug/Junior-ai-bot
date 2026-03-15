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
    """Routes requests to model specialists by lightweight complexity heuristics."""

    REALTIME_HINTS = {"latest", "real-time", "current", "news", "today", "now"}
    CODE_HINTS = {"refactor", "algorithm", "optimize", "architecture", "design"}

    def classify_complexity(self, task: str) -> Complexity:
        normalized = task.lower()
        token_count = len(normalized.split())

        if token_count > 80 or any(hint in normalized for hint in self.CODE_HINTS):
            return Complexity.HIGH
        if token_count > 30:
            return Complexity.MEDIUM
        return Complexity.LOW

    def choose_specialist(self, task: str) -> RouteDecision:
        normalized = task.lower()
        complexity = self.classify_complexity(task)

        if any(hint in normalized for hint in self.REALTIME_HINTS):
            return RouteDecision(
                specialist_key="grok_realtime",
                complexity=complexity,
                reason="Task asks for up-to-date or real-time information.",
            )

        if complexity is Complexity.HIGH:
            return RouteDecision(
                specialist_key="openai_logic",
                complexity=complexity,
                reason="High-complexity reasoning routed to OpenAI logic specialist.",
            )

        if complexity is Complexity.MEDIUM:
            return RouteDecision(
                specialist_key="gemini_analyst",
                complexity=complexity,
                reason="Medium-complexity analysis routed to Gemini specialist.",
            )

        return RouteDecision(
            specialist_key="openai_general",
            complexity=complexity,
            reason="Low-complexity task routed to GPT-4 generalist.",
        )
