# Junior-ai-bot

Super-Agent Orchestrator implementation in Python with LangChain + CrewAI.

## Features
- **Multi-model router** that chooses a specialist model based on task complexity and intent:
  - **GPT-7** for high-complexity logic/reasoning tasks.
  - **Gemini 5.3** for understanding and medium/low complexity interpretation.
  - **Grok** for real-time/current-events tasks.
- **Long-term memory** with `ChromaDB`.
- **Google Search tool** via Google Custom Search API.
- **GitHub file management tools** for reading/updating repository files.
- **CrewAI specialists** so each model runs as a role-based agent.

## Project structure

```text
super_agent_orchestrator/
  config.py
  models.py
  router.py
  memory.py
  crew.py
  orchestrator.py
  tools/
    search.py
    github_manager.py
main.py
```

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set environment variables:

```bash
export OPENAI_API_KEY=...
export GOOGLE_API_KEY=...
export GROK_API_KEY=...

# Optional model overrides
export OPENAI_LOGIC_MODEL=gpt-7
export GEMINI_UNDERSTANDING_MODEL=gemini-5.3
export GROK_MODEL=grok-beta

# Chroma
export CHROMA_COLLECTION=super_agent_memory
export CHROMA_DIR=./.chroma

# Google Custom Search
export GOOGLE_CSE_API_KEY=...
export GOOGLE_CSE_ID=...

# GitHub tools
export GITHUB_TOKEN=...
export GITHUB_REPO=owner/repo
```

3. Run:

```bash
python main.py
```

## Notes
- Router logic is in `super_agent_orchestrator/router.py` and can be extended with custom scoring/classifiers.
- Specialist model wiring is in `super_agent_orchestrator/models.py`.
- CrewAI role definitions are in `super_agent_orchestrator/crew.py`.
