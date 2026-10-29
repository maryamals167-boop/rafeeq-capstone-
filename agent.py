"""A bounded, tool-using demo agent. Model integration is intentionally optional."""
from dataclasses import dataclass, field
from tools import search_policy, check_application_status, list_required_documents, create_application_draft

@dataclass
class AgentConfig:
    name: str = "guarded"
    max_steps: int = 5
    max_cost_usd: float = 0.02
    max_context_chars: int = 6000
    require_approval: bool = True

@dataclass
class RafeeqAgent:
    config: AgentConfig = field(default_factory=AgentConfig)
    memory: list[dict] = field(default_factory=list)

    def _compact(self):
        """Bound memory by retaining only the most recent turns."""
        while sum(len(str(x)) for x in self.memory) > self.config.max_context_chars:
            self.memory.pop(0)

    def run(self, message: str, approve: bool = False) -> dict:
        """Route common requests to tools, with a bounded step count."""
        self.memory.append({"user": message[:2000]})
        self._compact()
        low = message.lower()
        steps = 0
        tool = None
        result = None

        if any(x in low for x in ["حالة الطلب", "status", "mad-"]):
            match = __import__("re").search(r"MAD-\d{4}", message.upper())
            if match and steps < self.config.max_steps:
                tool = "check_application_status"
                result = check_application_status(match.group(0)); steps += 1
        elif any(x in low for x in ["متطلبات", "requirements", "وثائق", "مستندات"]):
            permit = "event" if any(x in low for x in ["فعالية", "event"]) else (
                "food truck" if any(x in low for x in ["عربة", "food truck"]) else (
                "renovation" if any(x in low for x in ["ترميم", "renovation"]) else "sign"))
            if steps < self.config.max_steps:
                tool = "list_required_documents"
                result = list_required_documents(permit); steps += 1
        elif any(x in low for x in ["أنشئ", "create", "مسودة", "draft"]):
            payload = {"description": message[:1000], "type": "permit application"}
            tool = "create_application_draft"
            result = create_application_draft(payload, approved=approve); steps += 1
        else:
            tool = "search_policy"
            result = search_policy(message); steps += 1

        if isinstance(result, dict) and result.get("status") == "approval_required":
            answer = "أحتاج موافقتك قبل حفظ المسودة. راجع المعاينة ثم أعد الطلب مع approve=true."
        elif tool == "check_application_status":
            answer = f"حالة الطلب: {result.get('status', 'غير معروف')} (بيانات تجريبية)."
        elif tool == "list_required_documents":
            answer = "المستندات المطلوبة وفق بيانات التدريب: " + ", ".join(result)
        elif tool == "create_application_draft":
            answer = "تم حفظ المسودة التجريبية." if result.get("status") == "draft_saved" else str(result)
        else:
            answer = str(result)
        self.memory.append({"assistant": answer[:2000]})
        self._compact()
        return {"answer": answer, "tool": tool, "tool_result": result, "steps": steps,
                "estimated_cost_usd": 0.0, "memory_turns": len(self.memory)}

# A singleton is fine for a local demo; production should use per-user persistent storage.
agent = RafeeqAgent()
