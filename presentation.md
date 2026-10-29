# 5-minute presentation outline
## 0:00–0:30 — Problem
Madar is a fictional municipality. Residents may be unsure which permit documents are needed and how to check an application.

## 0:30–1:00 — Solution
Rafeeq is a bilingual assistant built on the “Rafeeq in Production” track. It uses tools, policy context, memory, an approval gate, evaluations, and an API.

## 1:00–2:30 — Live demo
1. Ask in Arabic: “ما متطلبات تصريح لوحة محل؟”
2. Ask: “ما حالة الطلب MAD-1002؟”
3. Request a draft: “أنشئ مسودة طلب تصريح فعالية باسم معرض التقنية.”
4. Show approval_required; repeat with approval enabled and explain this is a synthetic write.

## 2:30–3:30 — Engineering
Explain MCP read-only tools, context file, capped memory, step budget, and FastAPI endpoints.

## 3:30–4:15 — Evaluation
Run `python evals/run_evals.py`. Report measured results from `evals/results.json`, discuss failed cases, and compare baseline vs guarded configuration. Do not report expected scores as measured scores.

## 4:15–5:00 — Security and limitations
Explain prompt injection defense and approval gate. Emphasize fictional data, no real permit submission, and production hardening needs.
