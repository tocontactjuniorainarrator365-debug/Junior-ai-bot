from __future__ import annotations

from crewai import Agent, Crew, Task
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool


def build_specialist_agents(models: dict[str, BaseChatModel], tools: list[BaseTool]) -> dict[str, Agent]:
    """Build CrewAI agents mapped to specialist model roles."""

    return {
        "openai_general": Agent(
            role="GPT-4 Generalist",
            goal="Handle straightforward instructions quickly and accurately.",
            backstory="A practical assistant specialized in clear responses and drafting.",
            llm=models["openai_general"],
            tools=tools,
            verbose=True,
        ),
        "openai_logic": Agent(
            role="GPT-5 Logic Specialist",
            goal="Solve high-complexity logic and architecture tasks.",
            backstory="An expert systems thinker focused on rigorous reasoning.",
            llm=models["openai_logic"],
            tools=tools,
            verbose=True,
        ),
        "gemini_analyst": Agent(
            role="Gemini Analyst",
            goal="Perform structured analysis and synthesise findings.",
            backstory="A researcher that excels at balancing breadth and depth.",
            llm=models["gemini_analyst"],
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
