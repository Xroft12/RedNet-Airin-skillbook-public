from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional
import re

from .models import QMetaResult
from .memory import GraphMemory, ProcessTrace
from .safety import StrazhDoctrine


@dataclass
class ProcessOutput:
    name: str
    data: Dict[str, Any]
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "data": self.data, "notes": self.notes}


class MetaProcess:
    name = "meta_process"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        raise NotImplementedError


class MetaObserverProcess(MetaProcess):
    name = "meta_observer"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        warnings = []
        if result and result.branch and result.branch.loss > 0.5:
            warnings.append("выбранная ветвь имеет высокий loss; нужна ручная проверка")
        if any(w in task.lower() for w in ["срочно", "полностью", "все", "максимально"]):
            warnings.append("обнаружен широкий запрос; полезна декомпозиция и критерии приемки")
        return ProcessOutput(self.name, {"warnings": warnings, "task_length": len(task)}, ["фиксирует состояние процесса"])


class CriteriaLayerProcess(MetaProcess):
    name = "criteria_layer"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        criteria = list(context.get("criteria") or [])
        text = task.lower()
        if "библиотек" in text or "python" in text:
            criteria += ["импортируемость пакета", "работающие примеры", "тесты", "документация"]
        if "навык" in text:
            criteria += ["skill-card", "режим skill", "условия повторного применения"]
        if "безопас" in text or "страж" in text:
            criteria += ["permission-check", "audit-log", "simulation-only для опасных действий"]
        # preserve order, remove duplicates
        seen = set()
        uniq = []
        for c in criteria:
            if c not in seen:
                uniq.append(c); seen.add(c)
        return ProcessOutput(self.name, {"criteria": uniq}, ["извлекает критерии качества"])


class UncertaintyRegisterProcess(MetaProcess):
    name = "uncertainty_register"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        uncertainties = []
        if any(w in task.lower() for w in ["квант", "willow", "параллельн", "мультивселен"]):
            uncertainties.append({"item": "квантовые термины являются инженерной метафорой, если не подключён физический квантовый backend", "risk": "medium"})
        if result and result.skill and result.skill.get("confidence", 1) < 0.6:
            uncertainties.append({"item": "низкая уверенность кристаллизованного навыка", "risk": "medium"})
        return ProcessOutput(self.name, {"uncertainties": uncertainties}, ["не выдаёт гипотезы за доказанный факт"])


class DecisionMemoryProcess(MetaProcess):
    name = "decision_memory"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        decisions = []
        if result:
            decisions.append({"mode": result.mode.value, "selected_role": result.branch.role if result.branch else None})
        if context.get("mode_rule"):
            decisions.append({"mode_rule": context["mode_rule"]})
        return ProcessOutput(self.name, {"decisions": decisions}, ["сохраняет принятые решения"])


class UnfinishedMemoryProcess(MetaProcess):
    name = "unfinished_memory"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        items = []
        for marker in ["позже", "потом", "следующий шаг", "доработ", "исправ"]:
            if marker in task.lower():
                items.append({"marker": marker, "task": task[:200], "status": "open"})
        return ProcessOutput(self.name, {"items": items}, ["фиксирует хвосты и обещания"])


class ConversationBesedaProcess(MetaProcess):
    name = "beseda"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        should_ask = bool(context.get("allow_questions")) and len(task) < 30
        opinion = "Запрос лучше вести как совместное проектирование: сначала рабочий артефакт, затем уточнение и усиление."
        question = "Какой runtime/контейнер будет целевым для Гермеса?" if should_ask else None
        return ProcessOutput(self.name, {"opinion": opinion, "question": question}, ["задаёт вопросы только когда они меняют траекторию"])


class SourceLockProcess(MetaProcess):
    name = "source_lock_card"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        sources = context.get("sources") or []
        card = {
            "task": task[:200],
            "sources": sources,
            "boundary": "fact / hypothesis / metaphor / implementation must remain separated",
        }
        return ProcessOutput(self.name, card, ["фиксирует источники и границы интерпретации"])


class ChronologySynchronizer(MetaProcess):
    name = "chronology_synchronizer"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        branches = context.get("conversation_branches") or []
        stable_rules = []
        if "answer" in task.lower() or "skill" in task.lower():
            stable_rules.append("по умолчанию mode='answer'; навык создаётся только в mode='skill'")
        return ProcessOutput(self.name, {"branches_seen": len(branches), "stable_rules": stable_rules}, ["сверяет ветки и устойчивые правила"])


class WillowStabilityProcess(MetaProcess):
    name = "willow_stability"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        passes = int(context.get("willow_passes", 3))
        syndromes: List[Dict[str, Any]] = []
        for idx in range(passes):
            detected = []
            if result and result.branch and result.branch.loss > 0.25:
                detected.append("constraint_loss")
            if result and result.branch and not result.branch.evidence:
                detected.append("missing_evidence")
            if "квант" in task.lower() and "метафор" not in (result.answer or "").lower() if result and result.answer else False:
                detected.append("science_boundary_missing")
            syndromes.append({"pass": idx + 1, "detected": detected, "repair": "audit/clarify/simulation-boundary" if detected else "none"})
        return ProcessOutput(self.name, {"passes": passes, "syndromes": syndromes}, ["модель Willow: многопроходная коррекция ошибок, не физический QEC"])


class SanctumStateProcess(MetaProcess):
    name = "sanctum_state"

    def __init__(self) -> None:
        self.graph = GraphMemory()

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        node = self.graph.add_node("task", task[:80], {"mode": result.mode.value if result else None})
        if result and result.branch:
            bnode = self.graph.add_node("branch", result.branch.role, {"p": result.branch.probability_weight})
            self.graph.add_edge(node.id, bnode.id, "selected")
        return ProcessOutput(self.name, {"graph": self.graph.to_dict()}, ["Святилище как state/memory layer"])


class RedNetworkProcess(MetaProcess):
    name = "red_network_sim"

    def __init__(self) -> None:
        self.doctrine = StrazhDoctrine()

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        decision = self.doctrine.decide(task, context={"planet_scope": bool(context.get("planet_scope"))})
        return ProcessOutput(self.name, {"decision": decision.to_dict(), "journal_size": len(self.doctrine.journal)}, ["Красная сеть реализована как policy simulation + audit journal"])


class ResearchProtocolProcess(MetaProcess):
    name = "rednet_researcher"

    def run(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> ProcessOutput:
        protocol = [
            "separate established science from hypothesis and metaphor",
            "collect evidence",
            "run branches",
            "critical audit",
            "synthesize answer",
            "store process trace",
        ]
        return ProcessOutput(self.name, {"protocol": protocol}, ["исследовательская дисциплина для смелых концептов"])


class ProcessPipeline:
    def __init__(self, processes: Optional[Iterable[MetaProcess]] = None) -> None:
        self.processes = list(processes or [])
        self.trace = ProcessTrace()

    def run_all(self, task: str, result: Optional[QMetaResult], context: Dict[str, Any]) -> Dict[str, Any]:
        outputs = []
        for process in self.processes:
            output = process.run(task, result, context)
            outputs.append(output.to_dict())
            self.trace.record(process.name, "process executed", output=output.to_dict())
        return {"outputs": outputs, "trace": self.trace.to_list()}


def default_processes() -> List[MetaProcess]:
    return [
        MetaObserverProcess(),
        CriteriaLayerProcess(),
        UncertaintyRegisterProcess(),
        DecisionMemoryProcess(),
        UnfinishedMemoryProcess(),
        ConversationBesedaProcess(),
        SourceLockProcess(),
        ChronologySynchronizer(),
        WillowStabilityProcess(),
        SanctumStateProcess(),
        RedNetworkProcess(),
        ResearchProtocolProcess(),
    ]
