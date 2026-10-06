"""Controller: executes a JSON plan by invoking tool adapters sequentially.

Implements retries, simple error handling, and collects execution logs.
"""
from __future__ import annotations
import asyncio
import importlib
from typing import List
from src.agent.models import TaskEvent, validate_plan
from src.agent.task_graph import TaskGraph
from src.agent.verifier import verify_tool_output
from src.agent.tool_registry import default_tool_registry
from src.agent.recovery import should_retry
from src.utils.config import load_config


class Controller:
    def __init__(self, cfg=None, use_enhanced=True):
        self.cfg = cfg or load_config()
        self.events: List[TaskEvent] = []
        self.registry = default_tool_registry(use_enhanced=use_enhanced)
        self.tool_map = {
            name: self.registry.get(name).module_path
            for name in self.registry.names()
        }

    def get_events(self) -> List[TaskEvent]:
        return list(self.events)

    def _emit_event(self, event_type: str, message: str, task_id=None, **metadata):
        self.events.append(
            TaskEvent(
                event_type=event_type,
                task_id=str(task_id) if task_id is not None else None,
                message=message,
                metadata=metadata,
            )
        )

    async def execute_plan(self, plan: dict) -> List[str]:
        validated_plan = validate_plan(plan, self.registry)
        ordered_steps = TaskGraph(validated_plan.steps).ordered_steps()
        logs = []
        task_status = {}
        context = {"plan_input": validated_plan.input}
        self.events = []
        self._emit_event("plan_started", "Plan execution started")

        for step in ordered_steps:
            tool_name = step.tool
            args = step.args
            task_id = step.id
            task_key = str(task_id)
            blocked_by = [
                str(dependency)
                for dependency in step.dependencies
                if task_status.get(str(dependency)) != "COMPLETED"
            ]
            if blocked_by:
                task_status[task_key] = "SKIPPED"
                logs.append(f"Skipped step {task_id} -> {tool_name}: dependency failed")
                self._emit_event(
                    "task_skipped",
                    f"Skipped {tool_name}; dependency did not complete",
                    task_id=task_id,
                    tool=tool_name,
                    blocked_by=blocked_by,
                )
                continue

            logs.append(f"Starting step {task_id} -> {tool_name}")
            self._emit_event(
                "task_started",
                f"Started {tool_name}",
                task_id=task_id,
                tool=tool_name,
            )
            tool_spec = self.registry.get(tool_name)
            retry_count = 0
            while True:
                try:
                    tool_logs, output = await self._invoke_tool(tool_name, args, context)
                    for l in tool_logs:
                        logs.append(l)
                    verification = verify_tool_output(tool_name, output)
                    if not verification.verified:
                        raise ValueError(
                            "Verification failed: " + "; ".join(verification.issues)
                        )
                    self._emit_event(
                        "task_verified",
                        f"Verified {tool_name} output"
                        if retry_count == 0
                        else f"Verified {tool_name} output after retry",
                        task_id=task_id,
                        tool=tool_name,
                        confidence=verification.confidence,
                        evidence=verification.evidence,
                    )
                    if output is not None:
                        context[f"step_{task_id}_output"] = output
                    task_status[task_key] = "COMPLETED"
                    completion_label = "Finished step" if retry_count == 0 else "Finished retry step"
                    logs.append(f"{completion_label} {task_id} -> {tool_name}")
                    self._emit_event(
                        "task_completed",
                        f"Completed {tool_name}" if retry_count == 0 else f"Completed {tool_name} after retry",
                        task_id=task_id,
                        tool=tool_name,
                        retry_count=retry_count,
                    )
                    break
                except Exception as error:
                    failure_message = f"Error in step {task_id} ({tool_name}): {error}"
                    logs.append(failure_message)
                    self._emit_event(
                        "task_failed",
                        failure_message,
                        task_id=task_id,
                        tool=tool_name,
                        retry_count=retry_count,
                        error=str(error),
                    )
                    max_retries = tool_spec.max_retries if tool_spec else 0
                    if not should_retry(error, retry_count, max_retries):
                        task_status[task_key] = "FAILED"
                        break

                    retry_count += 1
                    logs.append(f"Retrying step {task_id} -> {tool_name} ({retry_count}/{max_retries})")
                    self._emit_event(
                        "recovery_started",
                        f"Retrying {tool_name}",
                        task_id=task_id,
                        tool=tool_name,
                        retry_count=retry_count,
                        max_retries=max_retries,
                    )
        self._emit_event("plan_completed", "Plan execution completed")
        return logs

    async def _invoke_tool(self, tool_name: str, args: dict, context: dict):
        tool = self.registry.get(tool_name)
        if not tool:
            raise ValueError(f"Unknown tool: {tool_name}")
        module_path = tool.module_path

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
