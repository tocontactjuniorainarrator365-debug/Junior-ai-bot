from __future__ import annotations

from crewai import Agent, Crew, Task
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool


def build_specialist_agents(models: dict[str, BaseChatModel], tools: list[BaseTool]) -> dict[str, Agent]:
    """Build CrewAI agents mapped to specialist model roles."""

    return {
        "openai_logic": Agent(
            role="GPT-7 Logic Specialist",
            goal="Solve high-complexity logic, planning, and architecture tasks.",
            backstory="An expert systems thinker focused on rigorous, stepwise reasoning.",
            llm=models["openai_logic"],
            tools=tools,
            verbose=True,
        ),
        "gemini_understanding": Agent(
            role="Gemini 5.3 Understanding Specialist",
            goal="Interpret user intent and produce clear, well-structured understanding outputs.",
            backstory="A semantic analyst that excels at contextual understanding and synthesis.",
            llm=models["gemini_understanding"],
            tools=tools,
            verbose=True,
        ),
        "grok_realtime": Agent(
            role="Grok Real-Time Specialist",
            goal="Handle current-events and rapidly changing information tasks.",
            backstory="A fast-moving analyst tuned for real-time context.",
            llm=models["grok_realtime"],
            tools=tools,
            verbose=True,
        ),
    }


def kickoff_with_specialist(agent: Agent, task_prompt: str) -> str:
    task = Task(
        description=task_prompt,
        expected_output="A complete, accurate response with concise rationale.",
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    return str(result)
