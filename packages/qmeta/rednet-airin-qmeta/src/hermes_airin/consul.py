from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence
import statistics

from .models import Branch
from .mathbase import tokenize, jaccard_kernel


@dataclass
class ExpertProfile:
    id: str
    name: str
    role: str
    priorities: List[str]
    weights: Dict[str, float] = field(default_factory=dict)


@dataclass
class ExpertOpinion:
    expert_id: str
    expert_name: str
    branch_id: str
    score_delta: float
    confidence: float
    notes: List[str]
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


@dataclass
class ConsulReport:
    opinions: List[ExpertOpinion]
    branch_adjustments: Dict[str, float]
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "opinions": [o.to_dict() for o in self.opinions],
            "branch_adjustments": self.branch_adjustments,
            "summary": self.summary,
        }


class Consul:
    """Council / Консул for multi-perspective branch review.

    The default experts are role-archetypes, not claims about real people.
    """

    def __init__(self, experts: Sequence[ExpertProfile] | None = None) -> None:
        self.experts = list(experts) if experts else self.default_experts()

    @staticmethod
    def default_experts() -> List[ExpertProfile]:
        return [
            ExpertProfile("architect", "Архитектор", "Собирает систему целиком", ["architecture", "interfaces", "maintainability"], {"architecture": 0.28, "tests": 0.12}),
            ExpertProfile("mathematician", "Математик", "Проверяет формализацию", ["model", "equations", "consistency"], {"model": 0.24, "formal": 0.18}),
            ExpertProfile("physicist", "Физик-корректор", "Разделяет физику, гипотезу и метафору", ["evidence", "science", "boundary"], {"evidence": 0.25, "risk": -0.10}),
            ExpertProfile("engineer", "Инженер", "Доводит идею до рабочего прототипа", ["code", "api", "tests", "docs"], {"code": 0.25, "tests": 0.2}),
            ExpertProfile("guardian", "ИБ-Страж", "Следит за разрешениями и побочными эффектами", ["safety", "permissions", "audit"], {"safety": 0.28, "permission": 0.25}),
            ExpertProfile("methodologist", "Методолог", "Сохраняет смысловую связность без выхода за научную границу", ["meaning", "model", "narrative"], {"meaning": 0.16, "model": 0.12}),
            ExpertProfile("memory", "Хранитель памяти", "Следит за следами процесса и переносом опыта", ["memory", "trace", "unfinished"], {"memory": 0.22, "trace": 0.16}),
            ExpertProfile("user_advocate", "Адвокат пользователя", "Проверяет, отвечает ли решение на реальную задачу", ["user", "answer", "practical"], {"answer": 0.25, "practical": 0.20}),
        ]

    def deliberate(self, task: str, branches: Sequence[Branch], context: Dict[str, Any] | None = None) -> ConsulReport:
        context = context or {}
        opinions: List[ExpertOpinion] = []
        for expert in self.experts:
            for branch in branches:
                opinions.append(self._opinion(expert, task, branch, context))
        adjustments: Dict[str, List[float]] = {}
        for opinion in opinions:
            adjustments.setdefault(opinion.branch_id, []).append(opinion.score_delta * opinion.confidence)
        averaged = {bid: statistics.mean(vals) if vals else 0.0 for bid, vals in adjustments.items()}
        for branch in branches:
            delta = averaged.get(branch.branch_id, 0.0)
            branch.score += delta
            branch.evidence.append(f"Consul: cumulative score delta {delta:.3f}")
            branch.add_trace("consul.adjust", "branch score adjusted by Consul", delta=delta)
        summary = self._summary(averaged)
        return ConsulReport(opinions=opinions, branch_adjustments=averaged, summary=summary)

    def _opinion(self, expert: ExpertProfile, task: str, branch: Branch, context: Dict[str, Any]) -> ExpertOpinion:
        text = " ".join([task, branch.role, branch.content, " ".join(branch.evidence)]).lower()
        tokens = tokenize(text)
        priority_overlap = sum(1 for p in expert.priorities if p.lower() in text)
        score_delta = 0.0
        notes: List[str] = []
        warnings: List[str] = []

        for key, weight in expert.weights.items():
            if key in text:
                score_delta += weight
                notes.append(f"усилен признак: {key}")

        if priority_overlap:
            score_delta += 0.05 * priority_overlap

        if expert.id == "physicist" and any(w in text for w in ["параллельн", "квант", "вселен"]):
            notes.append("нужно явно отделять физический факт от инженерной метафоры")
            if "метафор" not in text and "симуляц" not in text:
                warnings.append("нет границы между физикой и метафорой")
                score_delta -= 0.12

        if expert.id == "guardian" and branch.risk_profile.get("permission_decision", {}).get("allowed") is False:
            warnings.append("ветвь требует ограничения side-effects или simulation-only")
            score_delta -= 0.22

        if expert.id == "engineer" and not any(w in text for w in ["test", "тест", "api", "код", "пример"]):
            warnings.append("мало инженерных критериев приемки")
            score_delta -= 0.05

        if expert.id == "user_advocate":
            goal_text = " ".join(context.get("goals") or [])
            if goal_text:
                alignment = jaccard_kernel(goal_text, branch.content)
                score_delta += 0.15 * alignment
                notes.append(f"выравнивание с целями: {alignment:.2f}")

        confidence = min(1.0, 0.45 + 0.05 * len(notes) + 0.03 * priority_overlap)
        return ExpertOpinion(
            expert_id=expert.id,
            expert_name=expert.name,
            branch_id=branch.branch_id,
            score_delta=score_delta,
            confidence=confidence,
            notes=notes or ["нейтральная оценка"],
            warnings=warnings,
        )

    @staticmethod
    def _summary(adjustments: Dict[str, float]) -> str:
        if not adjustments:
            return "Консул не выявил ветвей для корректировки."
        best = max(adjustments.items(), key=lambda kv: kv[1])
        worst = min(adjustments.items(), key=lambda kv: kv[1])
        return f"Консул усилил ветвь {best[0]} ({best[1]:.3f}) и ослабил ветвь {worst[0]} ({worst[1]:.3f})."
