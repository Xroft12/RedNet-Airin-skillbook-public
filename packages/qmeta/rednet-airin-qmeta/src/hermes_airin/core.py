from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Sequence
import math

from .models import Branch, EngineState
from .skills import (
    branching_operator,
    audit_constraints_operator,
    score_operator,
    interference_operator,
    measure_operator,
)
from .safety import SafetyGuard
from .consul import Consul
from .mathbase import tokenize, phase_from_text

BranchGenerator = Callable[[str, Dict[str, Any]], List[Branch]]
Scorer = Callable[[Branch, Dict[str, Any]], float]


class BranchingMetaEngine:
    """Classical QMeta engine: branch -> audit -> score -> council -> interference -> measure."""

    def __init__(
        self,
        branch_generator: Optional[BranchGenerator] = None,
        scorer: Optional[Scorer] = None,
        safety_guard: Optional[SafetyGuard] = None,
        consul: Optional[Consul] = None,
        enable_consul: bool = True,
    ) -> None:
        self.branch_generator = branch_generator or default_branch_generator
        self.scorer = scorer or default_scorer
        self.safety_guard = safety_guard or SafetyGuard()
        self.consul = consul or Consul()
        self.enable_consul = enable_consul

    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> EngineState:
        context = dict(context or {})
        branches = branching_operator(task, context, self.branch_generator)
        branches = audit_constraints_operator(branches, context, self.safety_guard)
        branches = score_operator(branches, context, self.scorer)

        diagnostics: Dict[str, Any] = {}
        if self.enable_consul and context.get("enable_consul", True):
            report = self.consul.deliberate(task, branches, context)
            diagnostics["consul"] = report.to_dict()

        diagnostics["interference"] = interference_operator(branches, context)
        selected = measure_operator(branches, context)
        diagnostics["selected_branch_id"] = selected.branch_id
        diagnostics["branch_count"] = len(branches)
        return EngineState(task=task, context=context, branches=branches, selected=selected, diagnostics=diagnostics)


def default_branch_generator(task: str, context: Dict[str, Any]) -> List[Branch]:
    """Deterministic baseline branch generator.

    Production agents should replace this with an LLM branch generator.
    """
    goals = ", ".join(context.get("goals") or []) or "качество, проверяемость, безопасность"
    variants = [
        (
            "formal-model",
            f"Построить строгую модель задачи: выделить входы, выходы, ограничения, операторы, критерии успеха. Цели: {goals}. Задача: {task}",
            ["Формализация снижает риск красивого, но неисполняемого ответа."],
        ),
        (
            "engineering",
            f"Довести задачу до инженерного решения: API, структура модулей, тесты, примеры, документация, ограничения внедрения. Задача: {task}",
            ["Инженерная ветвь делает результат пригодным для разработки."],
        ),
        (
            "critical-audit",
            f"Проверить слабые места: где нет доказательств, где метафора смешивается с физикой, где возможны небезопасные побочные эффекты. Задача: {task}",
            ["Критическая ветвь нужна для декогеренции ошибочных решений."],
        ),
        (
            "prototype",
            f"Собрать минимальный рабочий прототип: классы, функции, сценарии использования, тестовые кейсы и расширяемые точки. Задача: {task}",
            ["Прототип позволяет проверить идею практически."],
        ),
        (
            "memory-process",
            f"Выделить память решений, процессные следы, незавершённые линии и синхронизацию веток. Задача: {task}",
            ["Память хранит не только текст, но и обязательства, критерии и причины решений."],
        ),
        (
            "safety-governance",
            f"Перевести сильные концепты в безопасную модель: permission-check, deny-by-default, журнал, симуляция вместо внешних действий. Задача: {task}",
            ["Контур Стража ограничивает побочные эффекты и защищает оператора."],
        ),
        (
            "consul-synthesis",
            f"Пропустить решение через Консул: математик, физик, инженер, ИБ-страж, методолог, хранитель памяти, адвокат пользователя. Задача: {task}",
            ["Совет экспертных контуров уменьшает односторонность ответа."],
        ),
    ]
    branches: List[Branch] = []
    base = 1.0 / math.sqrt(len(variants))
    for role, content, evidence in variants:
        b = Branch(content=content, role=role, evidence=evidence)
        b.phase = phase_from_text(role + task)
        b.amplitude = base * complex(math.cos(b.phase), math.sin(b.phase))
        branches.append(b)
    return branches


def default_scorer(branch: Branch, context: Dict[str, Any]) -> float:
    goals = set(tokenize(" ".join(context.get("goals") or [])))
    text_tokens = tokenize(branch.content + " " + branch.role)
    overlap = len(goals & text_tokens) / max(1, len(goals)) if goals else 0.25
    role_bonus = {
        "engineering": 0.22,
        "prototype": 0.20,
        "formal-model": 0.16,
        "safety-governance": 0.18,
        "memory-process": 0.14,
        "critical-audit": 0.10,
        "consul-synthesis": 0.12,
    }.get(branch.role, 0.08)
    evidence_bonus = min(0.18, 0.04 * len(branch.evidence))
    safety_penalty = 0.0
    if branch.constraints.get("simulation_only"):
        safety_penalty += 0.10
    return max(0.0, min(1.5, 0.35 + role_bonus + evidence_bonus + 0.35 * overlap - safety_penalty))


MultiverseEngine = BranchingMetaEngine
