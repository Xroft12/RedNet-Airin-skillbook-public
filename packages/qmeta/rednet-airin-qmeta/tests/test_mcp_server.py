from hermes_airin.mcp_server import qmeta_explain_model, qmeta_skill_catalog, qmeta_solve


def test_qmeta_solve_answer_tool_returns_serializable_result():
    result = qmeta_solve(
        task="Собери проверяемую модель ветвления решений.",
        mode="answer",
        context={"goals": ["проверяемость", "безопасность"]},
    )

    assert result["mode"] == "answer"
    assert result["answer"]
    assert result["diagnostics"]["branch_count"] > 0


def test_qmeta_skill_catalog_tool_lists_builtin_skills():
    result = qmeta_skill_catalog(query="meta")

    assert result["count"] > 0
    assert all("id" in skill for skill in result["skills"])


def test_qmeta_explain_model_states_scientific_boundary():
    result = qmeta_explain_model()

    assert result["type"] == "classical branching meta-skill engine"
    assert "does not claim quantum computation" in result["boundary"]
    assert result["side_effects"] == "none by default"
