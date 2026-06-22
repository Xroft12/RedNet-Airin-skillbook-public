from hermes_airin import HermesAirinAgent

agent = HermesAirinAgent()
result = agent.solve(
    "Создай мета-навык для параллельной проверки гипотез.",
    mode="skill",
    context={"new_skill_name": "parallel_hypothesis_solver"},
)
print(result.skill)
