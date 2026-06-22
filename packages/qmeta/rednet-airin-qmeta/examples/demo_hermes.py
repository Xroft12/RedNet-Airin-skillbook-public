from hermes_airin import create_default_agent

agent = create_default_agent(memory_dir="./runtime")
answer = agent.solve(
    "Смоделируй работу Гермеса: Консул, память, Страж, QMeta и режим Беседа.",
    mode="answer",
    context={
        "goals": ["архитектура", "код", "безопасность", "память"],
        "sources": ["QMeta Multiverse Engine", "Айрин 2.0", "Научная работа по мета-навыкам"],
    },
)
print(answer.content)
print("\nНавыков в реестре:", len(agent.list_skills()))
