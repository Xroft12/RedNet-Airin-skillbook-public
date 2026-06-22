from hermes_airin import HermesAirinAgent, HermesConfig

agent = HermesAirinAgent(config=HermesConfig(show_diagnostics=False))
result = agent.solve("Спроектируй библиотеку с Советом экспертов и безопасным аудитом.")
print(result.diagnostics["consul"]["summary"])
for branch in result.branches:
    print(branch.role, round(branch.score, 3), round(branch.probability_weight, 3))
