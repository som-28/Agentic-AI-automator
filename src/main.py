from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from src.agent.planner import Planner as RulePlanner
from src.agent.planner_llm import LLMPlanner
from src.agent.controller import Controller
from src.utils.config import load_config

app = FastAPI(title="Personal Task Automation Agent")

cfg = load_config()
# Use LLM planner if configured, else rule-based
planner_mode = os.getenv("PLANNER_MODE", "rule")
planner = LLMPlanner(cfg) if planner_mode == "llm" else RulePlanner(cfg)
controller = Controller(cfg)


class RunRequest(BaseModel):
    command: str
    email: Optional[str] = None


@app.post("/run")
async def run_task(req: RunRequest):
    try:
        plan = planner.plan(req.command, target_email=req.email)
        logs = await controller.execute_plan(plan)
        return {"plan": plan, "logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
