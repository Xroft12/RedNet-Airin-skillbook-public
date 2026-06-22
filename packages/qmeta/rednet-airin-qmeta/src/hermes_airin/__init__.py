"""Hermes / Airin QMeta library.

A classical, quantum-inspired meta-skill framework for agent orchestration.
"""

from .agent import HermesAirinAgent, QuantumInspiredAgent, HermesConfig, create_default_agent
from .models import Branch, MetaSkill, QMetaResult, QMetaMode, TraceEvent
from .core import BranchingMetaEngine, MultiverseEngine
from .consul import Consul, ExpertProfile, ExpertOpinion, ConsulReport
from .memory import JsonlMemory, GraphMemory, ProcessTrace
from .registry import SkillRegistry
from .safety import PermissionGate, SafetyGuard, StrazhDoctrine

__all__ = [
    "HermesAirinAgent",
    "QuantumInspiredAgent",
    "HermesConfig",
    "create_default_agent",
    "Branch",
    "MetaSkill",
    "QMetaResult",
    "QMetaMode",
    "TraceEvent",
    "BranchingMetaEngine",
    "MultiverseEngine",
    "Consul",
    "ExpertProfile",
    "ExpertOpinion",
    "ConsulReport",
    "JsonlMemory",
    "GraphMemory",
    "ProcessTrace",
    "SkillRegistry",
    "PermissionGate",
    "SafetyGuard",
    "StrazhDoctrine",
]

__version__ = "0.4.0"
