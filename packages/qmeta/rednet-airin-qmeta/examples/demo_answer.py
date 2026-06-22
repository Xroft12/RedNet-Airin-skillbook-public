from hermes_airin import HermesAirinAgent, HermesConfig

agent = HermesAirinAgent(config=HermesConfig(show_diagnostics=True))
result = agent.solve(
    "Разработай план проверки сложной научно-инженерной гипотезы через несколько ветвей.",
    mode="answer",
    context={"goals": ["план", "гипотезы", "проверка", "риски"]},
)
print(result.content)
