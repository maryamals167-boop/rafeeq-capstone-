# رفيق (Rafeeq) — SDAIA Agentic AI Capstone
**Track:** Rafeeq in Production  
**Author:** مريم هلال المطيري  
**Programme:** SDAIA Academy — Agentic AI Systems Engineering  
**Status:** runnable educational prototype; live model/MCP integration requires configuration.

Rafeeq is a bilingual (Arabic/English) municipal permit assistant for the fictional Madar municipality. It answers questions using synthetic policy context, can check permit requirements, inspect application status, and draft a permit application. A draft is a write action and requires explicit human approval before it is saved.

## Requirements covered
- Three domain tools plus an MCP tool (`search_policy` is exposed through the included MCP server).
- Context file: `context/municipal_policies.md`
- Conversation memory and bounded context compaction.
- Step and token/cost budget controls.
- Human approval gate for draft creation.
- 15 evaluation tasks run against two configurations (baseline and guarded).
- Security note covering the lethal trifecta, prompt-injection attack and defense.
- FastAPI service and basic health endpoint.

## Quick start
Python 3.11+

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app:app --reload
```
Open http://127.0.0.1:8000/docs

The default demo mode uses deterministic local behavior and does not require an API key. For real model calls, set `OPENROUTER_API_KEY` and `MODEL` in `.env`; then install optional `openai` package and use `RafeeqAgent(llm_enabled=True)`. Do not commit secrets.

## MCP server
Run separately:
```bash
python mcp_server.py
```
The MCP server exposes `search_policy` using stdio. It is intentionally read-only.

## Run evaluations
```bash
python evals/run_evals.py
```
This writes `evals/results.json` and prints summary scores. Results are not pre-filled: run them to capture actual outputs.

## Project layout
- `app.py` — FastAPI endpoint
- `agent.py` — bounded agent loop, tool routing, memory, approval gate
- `tools.py` — local tools
- `mcp_server.py` — MCP tool server
- `context/` — synthetic policy knowledge
- `evals/` — 15 task set and two configurations
- `docs/` — architecture, security and presentation notes

## Demo flow
1. Ask: `ما متطلبات تصريح لوحة محل؟`
2. Ask: `ما حالة الطلب MAD-1002؟`
3. Ask: `أنشئ مسودة طلب تصريح فعالية باسم معرض التقنية`
4. The agent returns an approval request. Confirm with `approve=true` to save the synthetic draft.

## Limitations
This is a prototype using fictional municipality data. It does not submit real permits, access government systems, or make legal determinations. Verify the generated evaluation output and add real model/provider credentials only if allowed by the programme.


## Official SDAIA references

- SDAIA Academy Agentic AI learning portal: https://sdaiaacademy.github.io/agentic-ai/
- SDAIA Academy Agentic AI capstone repository: https://github.com/SDAIAAcademy/agentic-ai/tree/main/labs/capstone
- SDAIA Academy official website: https://sdaia.gov.sa/ar/Sectors/BuildingCapacity/academy/Pages/default.aspx

Project author: **Maryam Helal Subhan**.

