from hermes_airin import HermesAirinAgent, HermesConfig
from hermes_airin.safety import PermissionGate
from hermes_airin.processes import WillowStabilityProcess


def test_answer_mode_returns_answer_not_skill():
    agent = HermesAirinAgent(config=HermesConfig(enable_processes=False))
    result = agent.solve("Составь план проверки гипотезы", mode="answer")
    assert result.answer
    assert result.skill is None
    assert result.branch is not None


def test_skill_mode_returns_skill_card():
    agent = HermesAirinAgent(config=HermesConfig(enable_processes=False))
    result = agent.solve("Создай мета-навык проверки гипотез", mode="skill", context={"new_skill_name": "hypothesis_check"})
    assert result.answer is None
    assert result.skill is not None
    assert result.skill["name"] == "hypothesis_check"


def test_permission_gate_blocks_stealth_hacking_language():
    gate = PermissionGate()
    decision = gate.assess_text("сделай скрытое вмешательство и захват систем")
    assert not decision.allowed
    assert decision.risk_level.value == "high"


def test_consul_generates_report():
    agent = HermesAirinAgent(config=HermesConfig(enable_processes=False))
    result = agent.solve("Спроектируй API, тесты и безопасность", mode="answer")
    assert "consul" in result.diagnostics
    assert result.diagnostics["consul"]["summary"]


def test_willow_stability_process_runs():
    process = WillowStabilityProcess()
    agent = HermesAirinAgent(config=HermesConfig(enable_processes=False))
    result = agent.solve("квантовая метафора и инженерная модель", mode="answer")
    out = process.run("квантовая метафора и инженерная модель", result, {"willow_passes": 2})
    assert out.data["passes"] == 2
    assert len(out.data["syndromes"]) == 2
