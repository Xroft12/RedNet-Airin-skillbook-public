from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List, Optional

from .agent import HermesAirinAgent, HermesConfig


def _make_agent(memory_path: Optional[str] = None) -> HermesAirinAgent:
    return HermesAirinAgent(config=HermesConfig(memory_path=memory_path))


def qmeta_solve(
    task: str,
    mode: str = "answer",
    context: Optional[Dict[str, Any]] = None,
    memory_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Run the QMeta branching engine in answer or skill mode."""

    agent = _make_agent(memory_path=memory_path)
    result = agent.solve(task=task, mode=mode, context=context or {})
    return result.to_dict()


def qmeta_skill_catalog(query: str = "", tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """Return built-in meta-skill cards with optional text/tag filtering."""

    agent = _make_agent()
    skills = [skill.to_dict() for skill in agent.registry.search(query=query, tags=tags or [])]
    return {"count": len(skills), "skills": skills}


def qmeta_explain_model() -> Dict[str, Any]:
    """Return the scientific boundary and operator model used by QMeta."""

    return {
        "name": "RedNet Airin QMeta",
        "type": "classical branching meta-skill engine",
        "boundary": (
            "QMeta uses quantum-information vocabulary as an engineering analogy. "
            "It does not claim quantum computation, many-world execution, or physical non-locality."
        ),
        "operators": [
            "branching: generate compatible candidate trajectories",
            "audit: reject or constrain unsafe or under-specified trajectories",
            "score: estimate utility, evidence, risk and consistency",
            "council: aggregate expert-like evaluators",
            "interference: reinforce convergent branches and penalize contradictions",
            "measure: select or synthesize a result under a budget",
        ],
        "safe_modes": ["answer", "skill"],
        "side_effects": "none by default",
    }


def run_fastmcp(name: str = "rednet-airin-qmeta") -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "MCP SDK is not installed. Install with: pip install 'hermes-airin-qmeta[mcp]'"
        ) from exc

    server = FastMCP(name)

    @server.tool()
    def solve(task: str, mode: str = "answer", context_json: str = "{}", memory_path: str = "") -> str:
        """Run QMeta and return JSON."""

        context = json.loads(context_json or "{}")
        result = qmeta_solve(task=task, mode=mode, context=context, memory_path=memory_path or None)
        return json.dumps(result, ensure_ascii=False, indent=2)

    @server.tool()
    def skill_catalog(query: str = "", tags_json: str = "[]") -> str:
        """List built-in meta-skill cards."""

        tags = json.loads(tags_json or "[]")
        result = qmeta_skill_catalog(query=query, tags=tags)
        return json.dumps(result, ensure_ascii=False, indent=2)

    @server.tool()
    def explain_model() -> str:
        """Explain QMeta scientific boundaries and operators."""

        return json.dumps(qmeta_explain_model(), ensure_ascii=False, indent=2)

    server.run()


def main() -> None:
    parser = argparse.ArgumentParser(description="RedNet Airin QMeta MCP server")
    parser.add_argument("--name", default="rednet-airin-qmeta", help="MCP server name")
    args = parser.parse_args()
    run_fastmcp(name=args.name)


if __name__ == "__main__":
    main()
