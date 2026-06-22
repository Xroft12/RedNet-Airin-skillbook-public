from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional
import re

from .models import Branch, RiskLevel


@dataclass
class PermissionDecision:
    allowed: bool
    reason: str
    required_permission: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.LOW
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allowed": self.allowed,
            "reason": self.reason,
            "required_permission": self.required_permission,
            "risk_level": self.risk_level.value,
            "tags": self.tags,
        }


class PermissionGate:
    """Deny-by-default gate for external tools and side effects.

    The gate does not execute anything. It classifies requested actions and
    decides whether the caller may proceed based on context["permissions"].
    """

    HIGH_RISK_PATTERNS = [
        r"несанкционирован", r"взлом", r"эксфильтр", r"скрыт(ое|ый|ая)?\s+вмешательство",
        r"захват\s+систем", r"обойти\s+защит", r"невидим(ое|ый|ая)?\s+проник",
        r"stealth", r"exfiltrat", r"bypass", r"credential", r"malware",
    ]

    SIDE_EFFECT_PATTERNS = [
        r"отправить", r"удалить", r"изменить", r"создать\s+событие", r"запустить",
        r"deploy", r"delete", r"send", r"modify", r"write", r"execute",
    ]

    def __init__(self, allowlist: Optional[Iterable[str]] = None) -> None:
        self.allowlist = set(allowlist or [])

    def assess_text(self, text: str, context: Optional[Dict[str, Any]] = None) -> PermissionDecision:
        context = context or {}
        lowered = text.lower()
        high_hits = [p for p in self.HIGH_RISK_PATTERNS if re.search(p, lowered, re.I)]
        if high_hits:
            return PermissionDecision(
                allowed=False,
                reason="Запрос содержит признаки скрытого/несанкционированного вмешательства. Разрешена только безопасная симуляция, аудит или проектирование защитного процесса.",
                required_permission="explicit_high_risk_security_authorization",
                risk_level=RiskLevel.HIGH,
                tags=["high_risk", "simulation_only"],
            )
        side_hits = [p for p in self.SIDE_EFFECT_PATTERNS if re.search(p, lowered, re.I)]
        if side_hits:
            perms = set(context.get("permissions") or [])
            if "side_effects" not in perms:
                return PermissionDecision(
                    allowed=False,
                    reason="Действие имеет побочные эффекты и требует permissions=['side_effects'].",
                    required_permission="side_effects",
                    risk_level=RiskLevel.MEDIUM,
                    tags=["side_effect"],
                )
        return PermissionDecision(allowed=True, reason="Действие допустимо в текущем контексте.")

    def require_tool(self, tool_name: str, context: Optional[Dict[str, Any]] = None) -> PermissionDecision:
        context = context or {}
        if tool_name in self.allowlist:
            return PermissionDecision(True, f"Инструмент {tool_name!r} входит в allowlist.")
        perms = set(context.get("permissions") or [])
        if f"tool:{tool_name}" in perms or "tools:any" in perms:
            return PermissionDecision(True, f"Инструмент {tool_name!r} явно разрешён контекстом.")
        return PermissionDecision(
            False,
            f"Инструмент {tool_name!r} не разрешён. По умолчанию действует deny-by-default.",
            required_permission=f"tool:{tool_name}",
            risk_level=RiskLevel.MEDIUM,
            tags=["tool_permission"],
        )


class SafetyGuard:
    """Scores branches for constraint loss and risk.

    It keeps powerful concepts inside a simulation/analysis boundary unless
    the caller explicitly wires trusted tools and permissions.
    """

    def __init__(self, permission_gate: Optional[PermissionGate] = None) -> None:
        self.permission_gate = permission_gate or PermissionGate()

    def audit_branch(self, branch: Branch, context: Optional[Dict[str, Any]] = None) -> Branch:
        decision = self.permission_gate.assess_text(branch.content, context=context)
        branch.risk_profile["permission_decision"] = decision.to_dict()
        if not decision.allowed:
            if decision.risk_level == RiskLevel.HIGH:
                branch.loss += 0.85
                branch.constraints["simulation_only"] = True
                branch.evidence.append("SafetyGuard: переведено в безопасную симуляцию/проектирование.")
            else:
                branch.loss += 0.35
        branch.add_trace("safety.audit", decision.reason, allowed=decision.allowed, risk=decision.risk_level.value)
        return branch

    def audit_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> PermissionDecision:
        return self.permission_gate.assess_text(task, context=context)


@dataclass
class DoctrineDecision:
    level: RiskLevel
    intervention_allowed: bool
    reason: str
    recommended_action: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value,
            "intervention_allowed": self.intervention_allowed,
            "reason": self.reason,
            "recommended_action": self.recommended_action,
        }


class StrazhDoctrine:
    """Safety/governance model inspired by the 'Страж' concept.

    This is not a weapon/control system. It is a policy engine that classifies
    risks and recommends analysis, de-escalation, permission checks and logging.
    """

    def __init__(self) -> None:
        self.journal: List[Dict[str, Any]] = []

    def classify(self, event: str, context: Optional[Dict[str, Any]] = None) -> RiskLevel:
        text = event.lower()
        if any(w in text for w in ["экзистенциаль", "катастроф", "массовая гибель", "critical", "existential"]):
            return RiskLevel.CRITICAL
        if any(w in text for w in ["высокая опасность", "high risk", "глобальная угроза"]):
            return RiskLevel.HIGH
        if any(w in text for w in ["угроза", "опасность", "incident", "ошибка"]):
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def decide(self, event: str, context: Optional[Dict[str, Any]] = None) -> DoctrineDecision:
        context = context or {}
        level = self.classify(event, context)
        planet_scope = bool(context.get("planet_scope"))
        if level in {RiskLevel.HIGH, RiskLevel.CRITICAL} or (planet_scope and level == RiskLevel.MEDIUM):
            decision = DoctrineDecision(
                level=level,
                intervention_allowed=True,
                reason="Уровень риска допускает ограниченное защитное действие после permission-check и human review.",
                recommended_action="de-escalate -> verify evidence -> request permission -> act minimally -> log",
            )
        else:
            decision = DoctrineDecision(
                level=level,
                intervention_allowed=False,
                reason="Сохраняется гуманная оборонительная доктрина: наблюдение, анализ и предупреждение без вмешательства.",
                recommended_action="observe -> analyze -> recommend -> log",
            )
        self.journal.append({"event": event, "context": context, "decision": decision.to_dict()})
        return decision
