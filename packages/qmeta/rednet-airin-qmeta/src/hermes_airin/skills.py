from __future__ import annotations

from typing import Any, Dict, List, Sequence
import hashlib

from .models import Branch, MetaSkill
from .mathbase import apply_interference, born_probabilities


class SkillCrystallizer:
    """Turns the selected branch trace into a reusable skill-card."""

    def crystallize(self, task: str, selected: Branch, context: Dict[str, Any] | None = None) -> MetaSkill:
        context = context or {}
        name = context.get("new_skill_name") or self._suggest_name(task, selected)
        digest = hashlib.sha256((name + task + selected.role).encode("utf-8", errors="ignore")).hexdigest()[:10]
        trace_ops = [t.operator for t in selected.trace]
        confidence = max(0.0, min(1.0, selected.probability_weight + selected.score * 0.15 - selected.loss * 0.20))
        return MetaSkill(
            id=f"skill.{name}.{digest}".replace(" ", "_").lower(),
            name=name,
            description=f"Reusable meta-skill crystallized from task: {task[:240]}",
            mode="skill",
            trigger=context.get("trigger", "similar problem structure"),
            operator_trace=trace_ops,
            selection_rule=context.get("selection_rule", "reuse when constraints and goals match"),
            inputs=["task", "context", "constraints", "memory"],
            outputs=["answer" if context.get("target_mode") == "answer" else "skill-card", "diagnostics", "process-trace"],
            safety=[
                "deny-by-default for side effects",
                "permission-check before tools",
                "separate fact/hypothesis/metaphor",
                "store trace without exposing hidden reasoning",
            ],
            confidence=confidence,
            tags=["qmeta", "metaskill", selected.role, "hermes", "airin"],
            metadata={
                "source_branch": selected.to_dict(),
                "task_hash": hashlib.sha256(task.encode("utf-8", errors="ignore")).hexdigest(),
            },
        )

    @staticmethod
    def _suggest_name(task: str, selected: Branch) -> str:
        base = selected.role.replace("-", "_").replace(" ", "_") or "meta_skill"
        if "гипот" in task.lower() or "hypothesis" in task.lower():
            return "parallel_hypothesis_solver"
        if "пам" in task.lower() or "memory" in task.lower():
            return "meta_memory_synchronizer"
        if "безопас" in task.lower() or "risk" in task.lower():
            return "strazh_risk_auditor"
        return f"{base}_skill"


def branching_operator(task: str, context: Dict[str, Any], generator) -> List[Branch]:
    branches = generator(task, context)
    for b in branches:
        b.add_trace("Sθ.branching", "branch generated", role=b.role)
    return branches


def audit_constraints_operator(branches: Sequence[Branch], context: Dict[str, Any], safety_guard) -> List[Branch]:
    return [safety_guard.audit_branch(b, context=context) for b in branches]


def score_operator(branches: Sequence[Branch], context: Dict[str, Any], scorer) -> List[Branch]:
    for b in branches:
        b.score = scorer(b, context)
        b.add_trace("Eω.score", "branch scored", score=b.score)
    return list(branches)


def interference_operator(branches: Sequence[Branch], context: Dict[str, Any]) -> Dict[str, Any]:
    matrix = apply_interference(
        branches,
        gamma=float(context.get("interference_gamma", 0.18)),
        eta=float(context.get("interference_eta", 0.30)),
        beta=float(context.get("interference_beta", 2.0)),
    )
    return {"matrix": matrix, "probabilities": born_probabilities(branches)}


def measure_operator(branches: Sequence[Branch], context: Dict[str, Any]) -> Branch:
    if not branches:
        raise ValueError("Cannot measure empty branch set")
    creative = bool(context.get("creative_measurement"))
    if not creative:
        selected = max(branches, key=lambda b: b.probability_weight)
        selected.add_trace("M.measure", "selected by argmax Born probability", probability=selected.probability_weight)
        return selected
    # Deterministic pseudo-sampling based on task hash for reproducibility.
    selected = max(branches, key=lambda b: b.probability_weight + 0.01 * len(b.content))
    selected.add_trace("M.measure", "selected by creative deterministic sampler", probability=selected.probability_weight)
    return selected


def answer_synthesizer(task: str, selected: Branch, branches: Sequence[Branch], context: Dict[str, Any]) -> str:
    visible_diag = context.get("show_diagnostics", False)
    lines = [
        f"## Ответ Гермес/Айрин",
        "",
        f"**Выбранная ветвь:** `{selected.role}`  ",
        f"**Вероятностный вес:** {selected.probability_weight:.3f}  ",
        "",
        selected.content.strip(),
    ]
    if selected.evidence:
        lines += ["", "### Основания", *[f"- {e}" for e in selected.evidence[:8]]]
    decision = selected.risk_profile.get("permission_decision") if selected.risk_profile else None
    if decision and decision.get("allowed") is False:
        lines += [
            "",
            "### Ограничение безопасности",
            decision.get("reason", "Ветвь ограничена политикой безопасности."),
        ]
    if visible_diag:
        lines += ["", "### Диагностика ветвей"]
        for b in branches:
            lines.append(f"- `{b.role}`: score={b.score:.3f}, loss={b.loss:.3f}, p={b.probability_weight:.3f}")
    return "\n".join(lines).strip()
