from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Protocol

from .models import Branch
from .safety import PermissionGate, PermissionDecision


class TextGenerator(Protocol):
    def __call__(self, prompt: str, context: Dict[str, Any]) -> str: ...


@dataclass
class LLMBranchGeneratorAdapter:
    """Adapter for replacing default branches with an external LLM.

    The callable is injected by the application. This package makes no network
    calls by itself.
    """

    generator: Callable[[str, Dict[str, Any]], Iterable[str]]
    roles: List[str] | None = None

    def __call__(self, task: str, context: Dict[str, Any]) -> List[Branch]:
        roles = self.roles or ["llm-branch"]
        raw = list(self.generator(task, context))
        branches = []
        for idx, content in enumerate(raw):
            role = roles[idx] if idx < len(roles) else f"llm-branch-{idx+1}"
            branches.append(Branch(content=content, role=role, evidence=["external LLM branch generator"]))
        return branches


@dataclass
class ToolSpec:
    name: str
    description: str
    side_effects: bool = False


class ToolManager:
    """Safe tool registry. It never executes non-allowed tools."""

    def __init__(self, permission_gate: PermissionGate | None = None) -> None:
        self.permission_gate = permission_gate or PermissionGate()
        self.tools: Dict[str, tuple[ToolSpec, Callable[..., Any]]] = {}

    def register(self, spec: ToolSpec, func: Callable[..., Any]) -> None:
        self.tools[spec.name] = (spec, func)

    def check(self, name: str, context: Dict[str, Any] | None = None) -> PermissionDecision:
        return self.permission_gate.require_tool(name, context=context)

    def call(self, name: str, *args: Any, context: Dict[str, Any] | None = None, **kwargs: Any) -> Any:
        decision = self.check(name, context=context)
        if not decision.allowed:
            raise PermissionError(decision.reason)
        spec, func = self.tools[name]
        if spec.side_effects:
            side = self.permission_gate.assess_text(f"execute side effect tool {name}", context=context)
            if not side.allowed:
                raise PermissionError(side.reason)
        return func(*args, **kwargs)
