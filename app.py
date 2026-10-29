from fastapi import FastAPI
from pydantic import BaseModel, Field
from agent import agent

app = FastAPI(title="Rafeeq — Madar Permit Assistant", version="1.0.0",
              description="Synthetic bilingual permit assistant capstone prototype.")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    approve: bool = False

@app.get("/health")
def health():
    return {"status": "ok", "service": "rafeeq", "mode": "synthetic-demo"}

@app.post("/chat")
def chat(req: ChatRequest):
    return agent.run(req.message, approve=req.approve)
