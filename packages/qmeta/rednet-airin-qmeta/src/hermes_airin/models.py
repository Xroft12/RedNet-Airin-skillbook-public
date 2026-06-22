from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid


class QMetaMode(str, Enum):
    ANSWER = "answer"
    SKILL = "skill"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class TraceEvent:
    operator: str
    note: str
    data: Dict[str, Any] = field(default_factory=dict)
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operator": self.operator,
            "note": self.note,
            "data": self.data,
            "ts": self.ts,
        }


@dataclass
class Branch:
    """A candidate trajectory of reasoning/solution.

    This is a classical structure that borrows quantum vocabulary:
    amplitude is a complex weight; probability follows |alpha|^2.
    """

    content: str
    role: str = "generic"
    evidence: List[str] = field(default_factory=list)
    risk_profile: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    trace: List[TraceEvent] = field(default_factory=list)
    score: float = 0.0
    loss: float = 0.0
    contradiction: float = 0.0
    amplitude: complex = complex(1.0, 0.0)
    phase: float = 0.0
    signature: str = ""
    branch_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])

    @property
    def probability_weight(self) -> float:
        return float(abs(self.amplitude) ** 2)

    @property
    def utility(self) -> float:
        return self.score - self.loss - self.contradiction

    def add_trace(self, operator: str, note: str, **data: Any) -> None:
        self.trace.append(TraceEvent(operator=operator, note=note, data=data))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "branch_id": self.branch_id,
            "role": self.role,
            "content": self.content,
            "evidence": list(self.evidence),
            "risk_profile": dict(self.risk_profile),
            "constraints": dict(self.constraints),
            "trace": [t.to_dict() for t in self.trace],
            "score": self.score,
            "loss": self.loss,
            "contradiction": self.contradiction,
            "amplitude": {"real": self.amplitude.real, "imag": self.amplitude.imag},
            "phase": self.phase,
            "signature": self.signature,
            "probability_weight": self.probability_weight,
            "utility": self.utility,
        }


@dataclass
class MetaSkill:
    id: str
    name: str
    description: str
    mode: str = "skill"
    trigger: str = "manual"
    operator_trace: List[str] = field(default_factory=list)
    selection_rule: str = "reuse when constraints and goals match"
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    safety: List[str] = field(default_factory=list)
    confidence: float = 0.0
    version: str = "0.3.0"
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "mode": self.mode,
            "trigger": self.trigger,
            "operator_trace": list(self.operator_trace),
            "selection_rule": self.selection_rule,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "safety": list(self.safety),
            "confidence": self.confidence,
            "version": self.version,
            "tags": list(self.tags),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetaSkill":
        return cls(**data)


@dataclass
class QMetaResult:
    mode: QMetaMode
    answer: Optional[str] = None
    skill: Optional[Dict[str, Any]] = None
    branch: Optional[Branch] = None
    branches: List[Branch] = field(default_factory=list)
    diagnostics: Dict[str, Any] = field(default_factory=dict)

    @property
    def content(self) -> str:
        if self.answer is not None:
            return self.answer
        if self.skill is not None:
            return str(self.skill)
        return ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode.value,
            "answer": self.answer,
            "skill": self.skill,
            "branch": self.branch.to_dict() if self.branch else None,
            "branches": [b.to_dict() for b in self.branches],
            "diagnostics": self.diagnostics,
        }


@dataclass
class EngineState:
    task: str
    context: Dict[str, Any]
    branches: List[Branch]
    selected: Branch
    diagnostics: Dict[str, Any]
