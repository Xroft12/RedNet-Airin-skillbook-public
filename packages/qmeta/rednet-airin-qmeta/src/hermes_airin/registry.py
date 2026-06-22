from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional
import importlib.resources as resources
import json

from .models import MetaSkill


class SkillRegistry:
    """Registry for meta-skills / skill-cards."""

    def __init__(self) -> None:
        self._skills: Dict[str, MetaSkill] = {}

    def register(self, skill: MetaSkill) -> MetaSkill:
        self._skills[skill.id] = skill
        return skill

    def get(self, skill_id: str) -> Optional[MetaSkill]:
        return self._skills.get(skill_id)

    def all(self) -> List[MetaSkill]:
        return list(self._skills.values())

    def search(self, query: str = "", tags: Optional[Iterable[str]] = None) -> List[MetaSkill]:
        tagset = set(tags or [])
        q = query.lower().strip()
        out = []
        for skill in self._skills.values():
            text = " ".join([skill.id, skill.name, skill.description, " ".join(skill.tags)]).lower()
            if q and q not in text:
                continue
            if tagset and not tagset.intersection(skill.tags):
                continue
            out.append(skill)
        return out

    def load_json_dir(self, path: str | Path) -> int:
        count = 0
        for p in Path(path).glob("*.json"):
            data = json.loads(p.read_text(encoding="utf-8"))
            self.register(MetaSkill.from_dict(data))
            count += 1
        return count

    def load_builtin(self) -> int:
        count = 0
        try:
            base = resources.files("hermes_airin.skill_cards")
            for file in base.iterdir():
                if file.name.endswith(".json"):
                    data = json.loads(file.read_text(encoding="utf-8"))
                    self.register(MetaSkill.from_dict(data))
                    count += 1
        except Exception:
            return count
        return count

    def save_json_dir(self, path: str | Path) -> int:
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        for skill in self._skills.values():
            (target / f"{skill.id}.json").write_text(json.dumps(skill.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return len(self._skills)
