"""Controller: executes a JSON plan by invoking tool adapters sequentially.

Implements retries, simple error handling, and collects execution logs.
"""
from __future__ import annotations
import asyncio
import importlib
from typing import List
from src.utils.config import load_config


class Controller:
    def __init__(self, cfg=None, use_enhanced=True):
        self.cfg = cfg or load_config()
        # tool registry maps tool name to module path
        # Use enhanced tools if available
        if use_enhanced:
            self.tool_map = {
                "search": "src.tools.search_tool_enhanced",
                "scrape": "src.tools.scraper_tool_enhanced",
                "summarize": "src.tools.summarizer_tool",
                "summarise": "src.tools.summarizer_tool",
                "email": "src.tools.email_tool",
                "logger": "src.tools.logger_tool",
                "resume_parser": "src.tools.resume_parser_tool",
                "resume_analyzer": "src.tools.resume_analyzer_tool",
                "job_matcher": "src.tools.job_matcher_tool",
            }
        else:
            self.tool_map = {
                "search": "src.tools.search_tool",
                "scrape": "src.tools.scraper_tool",
                "summarize": "src.tools.summarizer_tool",
                "summarise": "src.tools.summarizer_tool",
                "email": "src.tools.email_tool",
                "logger": "src.tools.logger_tool",
                "resume_parser": "src.tools.resume_parser_tool",
                "resume_analyzer": "src.tools.resume_analyzer_tool",
                "job_matcher": "src.tools.job_matcher_tool",
            }

    async def execute_plan(self, plan: dict) -> List[str]:
        logs = []
        steps = plan.get("steps", [])
        context = {"plan_input": plan.get("input")}

        for step in steps:
            tool_name = step.get("tool")
            args = step.get("args", {})
            logs.append(f"Starting step {step.get('id')} -> {tool_name}")
            try:
                tool_logs, output = await self._invoke_tool(tool_name, args, context)
                for l in tool_logs:
                    logs.append(l)
                # optionally store results in context
                if output is not None:
                    context_key = f"step_{step.get('id')}_output"
                    context[context_key] = output
                logs.append(f"Finished step {step.get('id')} -> {tool_name}")
            except Exception as e:
                err = f"Error in step {step.get('id')} ({tool_name}): {e}"
                logs.append(err)
                # retry once for transient errors
                logs.append(f"Retrying step {step.get('id')} -> {tool_name}")
                try:
                    tool_logs, output = await self._invoke_tool(tool_name, args, context)
                    for l in tool_logs:
                        logs.append(l)
                    if output is not None:
                        context[f"step_{step.get('id')}_output"] = output
                    logs.append(f"Finished retry step {step.get('id')} -> {tool_name}")
                except Exception as e2:
                    logs.append(f"Failed retry for step {step.get('id')}: {e2}")
                    # continue to next step
        return logs

    async def _invoke_tool(self, tool_name: str, args: dict, context: dict):
        module_path = self.tool_map.get(tool_name)
        if not module_path:
            raise ValueError(f"Unknown tool: {tool_name}")

        module = importlib.import_module(module_path)
        # Each tool exposes a class named <CamelCase>Tool, but we provide a runtime function run()
        if hasattr(module, "run"):
            # run may be sync or async
            fn = getattr(module, "run")
            if asyncio.iscoroutinefunction(fn):
                return await fn(args, context)
            else:
                # run in threadpool
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, lambda: fn(args, context))
        elif hasattr(module, "Tool"):
            ToolCls = getattr(module, "Tool")
            inst = ToolCls(self.cfg)
            if asyncio.iscoroutinefunction(inst.run):
                return await inst.run(args, context)
            else:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, lambda: inst.run(args, context))
        else:
            raise ValueError(f"Tool module {module_path} missing run() or Tool class")
