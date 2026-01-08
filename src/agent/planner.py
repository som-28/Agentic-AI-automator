"""Planner: convert natural language tasks into a JSON execution plan.

This planner is rule-based for offline demo use. If an OpenAI key is provided,
it will optionally call the LLM to improve plans.
"""
from __future__ import annotations
import re
import os
import json
from src.utils.config import load_config


class Planner:
    def __init__(self, cfg=None):
        self.cfg = cfg or load_config()

    def plan(self, command: str, target_email: str | None = None) -> dict:
        """Produce a JSON plan with ordered steps.

        Sample plan structure:
        {
            "input": "...",
            "steps": [
                {"id": 1, "tool": "search", "args": {...}},
                {"id": 2, "tool": "scrape", "args": {...}},
                {"id": 3, "tool": "summarize", "args": {...}},
                {"id": 4, "tool": "email", "args": {...}}
            ]
        }
        """
        cmd = command.lower()
        steps = []
        sid = 1

        # detect 'search' intent
        if any(k in cmd for k in ["find", "search", "look for", "top", "list"]):
            # determine query phrase
            q = self._extract_search_query(command)
            steps.append({"id": sid, "tool": "search", "args": {"query": q, "limit": 5}})
            sid += 1

        # detect 'scrape' or need to open links
        if any(k in cmd for k in ["scrape", "details", "summarize", "summary", "compare"]) or "internship" in cmd or "course" in cmd:
            # Add a scraping step to fetch details from search results
            steps.append({"id": sid, "tool": "scrape", "args": {"top_k": 3}})
            sid += 1

        # detect summarization
        if any(k in cmd for k in ["summarize", "summary", "bullet", "compare", "comparison"]):
            steps.append({"id": sid, "tool": "summarize", "args": {"mode": "bullet", "max_sentences": 8}})
            sid += 1

        # email
        if target_email or "email" in cmd or "send" in cmd:
            steps.append({"id": sid, "tool": "email", "args": {"to": target_email or "", "subject": f"Automation result for: {command}"}})
            sid += 1

        # always log
        steps.append({"id": sid, "tool": "logger", "args": {"message": f"Completed task: {command}"}})

        plan = {"input": command, "steps": steps}

        return plan

    def _extract_search_query(self, command: str) -> str:
        # Very simple heuristics for common queries
        # For example: "Find me top 5 internships in Bangalore" -> "top internships in Bangalore"
        patterns = [r"find me (.+)", r"search for (.+)", r"look for (.+)", r"find (.+)"]
        for p in patterns:
            m = re.search(p, command, re.IGNORECASE)
            if m:
                return m.group(1)
        # fallback: whole command
        return command
