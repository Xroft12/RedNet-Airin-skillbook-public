from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from .core import MultiverseEngine
from .models import QMetaMode, QMetaResult
from .skills import SkillCrystallizer, answer_synthesizer
from .memory import JsonlMemory
from .registry import SkillRegistry
from .processes import ProcessPipeline, default_processes
from .safety import PermissionGate, SafetyGuard
from .consul import Consul


@dataclass
class HermesConfig:
    memory_path: Optional[str] = None
    enable_consul: bool = True
    enable_processes: bool = True
    show_diagnostics: bool = False
    default_mode: str = "answer"
    permissions: list[str] = field(default_factory=list)


class QuantumInspiredAgent:
    """Base QMeta agent with two result modes: answer and skill."""

    def __init__(
        self,
        engine: Optional[MultiverseEngine] = None,
        registry: Optional[SkillRegistry] = None,
        memory: Optional[JsonlMemory] = None,
        config: Optional[HermesConfig] = None,
    ) -> None:
        self.config = config or HermesConfig()
        self.registry = registry or SkillRegistry()
        self.registry.load_builtin()
        self.memory = memory or (JsonlMemory(self.config.memory_path) if self.config.memory_path else None)
        self.engine = engine or MultiverseEngine(enable_consul=self.config.enable_consul)
        self.crystallizer = SkillCrystallizer()

    def solve(self, task: str, mode: str | QMetaMode = "answer", context: Optional[Dict[str, Any]] = None) -> QMetaResult:
        context = dict(context or {})
        if isinstance(mode, str):
            mode = QMetaMode(mode)
        context.setdefault("permissions", self.config.permissions)
        context.setdefault("show_diagnostics", self.config.show_diagnostics)
        context.setdefault("mode_rule", "answer by default; skill only when explicitly requested")

        state = self.engine.run(task, context=context)
        if mode == QMetaMode.ANSWER:
            answer = answer_synthesizer(task, state.selected, state.branches, context)
            result = QMetaResult(mode=mode, answer=answer, skill=None, branch=state.selected, branches=state.branches, diagnostics=state.diagnostics)
        elif mode == QMetaMode.SKILL:
            skill = self.crystallizer.crystallize(task, state.selected, context=context)
            self.registry.register(skill)
            result = QMetaResult(mode=mode, answer=None, skill=skill.to_dict(), branch=state.selected, branches=state.branches, diagnostics=state.diagnostics)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        if self.memory:
            self.memory.append("qmeta_result", result.to_dict(), tags=[mode.value, "qmeta", "hermes_airin"])
        return result


class HermesAirinAgent(QuantumInspiredAgent):
    """Hermes/Airin specialized agent with Consul, processes, memory and safety."""

    def __init__(self, config: Optional[HermesConfig] = None, **kwargs: Any) -> None:
        config = config or HermesConfig()
        permission_gate = PermissionGate()
        safety_guard = SafetyGuard(permission_gate)
        consul = Consul()
        engine = kwargs.pop("engine", None) or MultiverseEngine(safety_guard=safety_guard, consul=consul, enable_consul=config.enable_consul)
        super().__init__(engine=engine, config=config, **kwargs)
        self.process_pipeline = ProcessPipeline(default_processes()) if config.enable_processes else None

    def solve(self, task: str, mode: str | QMetaMode = "answer", context: Optional[Dict[str, Any]] = None) -> QMetaResult:
        result = super().solve(task=task, mode=mode, context=context)
        if self.process_pipeline:
            process_diag = self.process_pipeline.run_all(task, result, dict(context or {}))
            result.diagnostics["processes"] = process_diag
            if self.memory:
                self.memory.append("process_diagnostics", process_diag, tags=["process", "hermes_airin"])
        return result

    def list_skills(self) -> list[dict[str, Any]]:
        return [s.to_dict() for s in self.registry.all()]


def create_default_agent(memory_dir: str | Path | None = None) -> HermesAirinAgent:
    memory_path = None
    if memory_dir:
        memory_path = str(Path(memory_dir) / "hermes_airin_memory.jsonl")
    return HermesAirinAgent(config=HermesConfig(memory_path=memory_path))
