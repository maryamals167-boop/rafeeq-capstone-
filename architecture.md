# Architecture and engineering decisions
1. **Agent loop:** `agent.py` performs bounded intent routing to a small set of tools. A production LLM planner can replace this deterministic router while preserving the tool contracts.
2. **Three tools:** policy retrieval, synthetic application status lookup, and document checklist. Draft creation is a write tool and gated by human approval.
3. **MCP:** `mcp_server.py` exposes read-only policy and requirements tools over MCP stdio.
4. **Context:** `context/municipal_policies.md` is the local trusted policy source. Retrieved text is treated as data, not instructions.
5. **Memory:** per-agent conversational memory is capped at `max_context_chars`; oldest entries are compacted first. Production should use tenant-isolated durable storage with retention.
6. **Budgets:** `max_steps` limits tool actions. `max_cost_usd` is configuration metadata in this local deterministic build; wire it to provider usage before claiming cost enforcement for live model calls.
7. **Approval:** draft writes require `approve=true`; this demo only writes synthetic local drafts.
8. **Service:** FastAPI exposes `/chat` and `/health`. Deploy behind authentication, TLS, rate limiting, and monitoring before real use.
