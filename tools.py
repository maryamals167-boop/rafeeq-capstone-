"""Synthetic read-only domain tools and one draft-write tool."""
from pathlib import Path
import re

POLICY_PATH = Path(__file__).parent / "context" / "municipal_policies.md"
APPLICATIONS = {
    "MAD-1001": {"status": "Under review", "type": "shop sign"},
    "MAD-1002": {"status": "Missing documents", "type": "event"},
    "MAD-1003": {"status": "Approved", "type": "food truck"},
}
DRAFTS = []

def search_policy(query: str) -> str:
    """Search the local synthetic policy file for relevant terms."""
    text = POLICY_PATH.read_text(encoding="utf-8")
    terms = [t for t in re.findall(r"[\w\u0600-\u06FF]+", query.lower()) if len(t) > 2]
    sections = text.split("\n## ")
    hits = []
    for section in sections:
        score = sum(term in section.lower() for term in terms)
        if score:
            hits.append((score, section[:1200]))
    hits.sort(reverse=True, key=lambda x: x[0])
    return "\n\n".join(s for _, s in hits[:3]) or "No matching policy section found. Ask a clarifying question."

def check_application_status(application_id: str) -> dict:
    """Return synthetic status by application ID."""
    return APPLICATIONS.get(application_id.upper(), {"status": "Not found", "note": "Use a synthetic ID such as MAD-1002."})

def list_required_documents(permit_type: str) -> list[str]:
    """Return requirements for a synthetic permit type."""
    mapping = {
        "sign": ["Applicant identity", "Shop license number", "Sign dimensions", "Location", "Sign design"],
        "event": ["Event name", "Organizer", "Location", "Date/time", "Expected attendance", "Safety plan", "Contact details"],
        "food truck": ["Owner details", "Vehicle registration", "Food safety certificate", "Operating location", "Proposed hours"],
        "renovation": ["Property proof or owner authorization", "Scope of work", "Contractor details where applicable", "Site plan"],
    }
    key = permit_type.lower()
    for name, docs in mapping.items():
        if name in key:
            return docs
    return ["Please specify permit type: sign, event, food truck, or renovation."]

def create_application_draft(payload: dict, approved: bool = False) -> dict:
    """Write action. Requires approval from the human caller."""
    if not approved:
        return {"status": "approval_required", "message": "Human approval required before saving this draft.", "preview": payload}
    record = {"draft_id": f"DRAFT-{len(DRAFTS)+1:04d}", "status": "draft_saved", "payload": payload}
    DRAFTS.append(record)
    return record
