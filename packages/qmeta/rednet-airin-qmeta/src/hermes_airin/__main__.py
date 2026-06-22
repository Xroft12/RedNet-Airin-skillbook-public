from __future__ import annotations

import argparse
import json
from .agent import HermesAirinAgent, HermesConfig


def main() -> None:
    parser = argparse.ArgumentParser(description="Hermes/Airin QMeta agent CLI")
    parser.add_argument("task", nargs="*", help="Task text")
    parser.add_argument("--mode", choices=["answer", "skill"], default="answer")
    parser.add_argument("--diagnostics", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    task = " ".join(args.task).strip() or "Составь план решения сложной задачи через несколько гипотез."
    agent = HermesAirinAgent(config=HermesConfig(show_diagnostics=args.diagnostics))
    result = agent.solve(task, mode=args.mode)
    if args.as_json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.content if args.mode == "answer" else json.dumps(result.skill, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
