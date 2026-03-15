from super_agent_orchestrator import SuperAgentOrchestrator


if __name__ == "__main__":
    orchestrator = SuperAgentOrchestrator()
    task = "Design a modular CI/CD strategy for a Python monorepo and include rollout safeguards."
    response = orchestrator.run(task)

    print(f"Specialist used: {response.specialist}")
    print(f"Reason: {response.route_reason}")
    print("Output:")
    print(response.output)
