"""LLM-based planner using OpenAI to decompose complex tasks.

Falls back to rule-based planning if no OpenAI key is configured.
"""
from __future__ import annotations
import os
import json
import re
from src.utils.config import load_config

# Import the rule-based planner logic
from src.agent.planner import Planner as RulePlanner


class LLMPlanner:
    def __init__(self, cfg=None):
        self.cfg = cfg or load_config()
        self.rule_planner = RulePlanner(cfg)
    
    def plan(self, command: str, target_email: str | None = None) -> dict:
        """Generate plan using LLM if available, else rule-based."""
        planner_mode = os.getenv("PLANNER_MODE", "rule")
        
        if planner_mode == "llm" and os.getenv("OPENAI_API_KEY"):
            return self._plan_with_llm(command, target_email)
        else:
            return self.rule_planner.plan(command, target_email)
    
    def _plan_with_llm(self, command: str, target_email: str | None = None) -> dict:
        """Use OpenAI to generate a detailed execution plan."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            system_prompt = """You are a task planning agent. Given a user command, break it down into ordered steps using these tools:

Available tools:
- search: Search the web for information. Args: {"query": str, "limit": int}
- scrape: Scrape web pages for details. Args: {"top_k": int} or {"url": str}
- summarize: Summarize gathered information. Args: {"mode": "bullet"|"comparison", "max_sentences": int}
- email: Send email with results. Args: {"to": str, "subject": str, "body": str (optional)}
- logger: Log completion message. Args: {"message": str}

Return ONLY a valid JSON object with this structure:
{
  "input": "<original command>",
  "steps": [
    {"id": 1, "tool": "search", "args": {...}},
    {"id": 2, "tool": "scrape", "args": {...}},
    ...
  ]
}

Be specific with queries and arguments. Do not include markdown formatting or explanations."""

            user_prompt = f"Command: {command}"
            if target_email:
                user_prompt += f"\nTarget email: {target_email}"
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=800,
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from potential markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            plan = json.loads(content)
            
            # Ensure plan has required structure
            if "input" not in plan:
                plan["input"] = command
            if "steps" not in plan or not isinstance(plan["steps"], list):
                raise ValueError("Invalid plan structure")
            
            # Add target email if provided and not already in plan
            if target_email:
                has_email_step = any(s.get("tool") == "email" for s in plan["steps"])
                if has_email_step:
                    for step in plan["steps"]:
                        if step.get("tool") == "email" and "to" in step.get("args", {}):
                            if not step["args"]["to"]:
                                step["args"]["to"] = target_email
            
            return plan
        
        except Exception as e:
            print(f"LLM planning failed: {e}, falling back to rule-based planner")
            return self.rule_planner.plan(command, target_email)
