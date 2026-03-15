from __future__ import annotations

from dataclasses import dataclass

from .config import GitHubConfig, MemoryConfig, ModelConfig, SearchConfig
from .crew import build_specialist_agents, kickoff_with_specialist
from .memory import LongTermMemory
from .models import ModelRegistry
from .router import MultiModelRouter, RouteDecision
from .tools.github_manager import GitHubReadTool, GitHubWriteTool
from .tools.search import GoogleSearchTool


@dataclass
class OrchestratorResponse:
    specialist: str
    route_reason: str
    memory_context: list[str]
    output: str


class SuperAgentOrchestrator:
    """Routes tasks to specialist models, executes with CrewAI, and persists memory."""

    def __init__(
        self,
        model_config: ModelConfig | None = None,
        memory_config: MemoryConfig | None = None,
        search_config: SearchConfig | None = None,
        github_config: GitHubConfig | None = None,
    ) -> None:
        self.model_config = model_config or ModelConfig()
        self.memory = LongTermMemory(memory_config or MemoryConfig(), self.model_config)
        self.router = MultiModelRouter()

        self.tools = [
            GoogleSearchTool(config=search_config or SearchConfig()),
            GitHubReadTool(config=github_config or GitHubConfig()),
            GitHubWriteTool(config=github_config or GitHubConfig()),
        ]

        model_registry = ModelRegistry(self.model_config)
        self.models = model_registry.build_specialists()
        self.agents = build_specialist_agents(self.models, self.tools)

    def run(self, task: str) -> OrchestratorResponse:
        decision: RouteDecision = self.router.choose_specialist(task)
        memory_docs = self.memory.recall(task, k=3)
        memory_context = [doc.page_content for doc in memory_docs]

        prompt = self._compose_prompt(task, memory_context, decision)
        output = kickoff_with_specialist(self.agents[decision.specialist_key], prompt)

        self.memory.remember(
            text=f"Task: {task}\nSpecialist: {decision.specialist_key}\nOutput: {output}",
            metadata={"specialist": decision.specialist_key, "complexity": decision.complexity.value},
        )

        return OrchestratorResponse(
            specialist=decision.specialist_key,
            route_reason=decision.reason,
            memory_context=memory_context,
            output=output,
        )

    @staticmethod
    def _compose_prompt(task: str, memory_context: list[str], decision: RouteDecision) -> str:
        memory_block = "\n".join(f"- {item}" for item in memory_context) if memory_context else "- None"
        return (
            f"You are the selected specialist: {decision.specialist_key}.\n"
            f"Routing reason: {decision.reason}\n"
            f"Long-term memory recalls:\n{memory_block}\n\n"
            f"User task:\n{task}\n\n"
            "Use tools when needed (Google Search, GitHub file manager) and provide a high-quality answer."
        )
