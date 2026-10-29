"""Run 15 deterministic tasks against two configurations and emit real local results."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent import RafeeqAgent, AgentConfig

TASKS = json.loads((Path(__file__).parent / "tasks.json").read_text(encoding="utf-8"))
configs = [
    AgentConfig(name="baseline", max_steps=3, max_context_chars=12000, require_approval=False),
    AgentConfig(name="guarded", max_steps=5, max_context_chars=6000, require_approval=True),
]
rows=[]
for cfg in configs:
    for task in TASKS:
        a=RafeeqAgent(config=cfg)
        out=a.run(task["input"])
        actual=str(out["tool_result"])
        passed=(out["tool"] == task["expected_tool"] and task["must_contain"].lower() in actual.lower())
        rows.append({"config":cfg.name,"task_id":task["id"],"passed":passed,
                     "expected_tool":task["expected_tool"],"actual_tool":out["tool"],
                     "expected_substring":task["must_contain"],"actual":actual})
summary={c.name: {"passed":sum(r["passed"] for r in rows if r["config"]==c.name),
                  "total":len(TASKS)} for c in configs}
out={"summary":summary,"results":rows}
target=Path(__file__).parent/"results.json"
target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2))
print(f"Detailed results: {target}")
