"""Dependency-aware ordering for execution plans."""
from __future__ import annotations

from typing import Dict, List, Set

from src.agent.models import PlanStep


class TaskGraph:
    def __init__(self, steps: List[PlanStep]):
        self.steps: Dict[str, PlanStep] = {str(step.id): step for step in steps}
        self._validate_acyclic()

    def ordered_steps(self) -> List[PlanStep]:
        ordered: List[PlanStep] = []
        remaining = set(self.steps)
        completed: Set[str] = set()

        while remaining:
            ready = [
                self.steps[task_id]
                for task_id in remaining
                if {str(dep) for dep in self.steps[task_id].dependencies} <= completed
            ]
            if not ready:
                raise ValueError("Task graph cannot resolve its dependencies")
            ready.sort(key=lambda step: str(step.id))
            ordered.extend(ready)
            completed.update(str(step.id) for step in ready)
            remaining.difference_update(str(step.id) for step in ready)

        return ordered

    def _validate_acyclic(self) -> None:
        visiting: Set[str] = set()
        visited: Set[str] = set()

        def visit(task_id: str) -> None:
            if task_id in visiting:
                raise ValueError("Task graph contains a dependency cycle")
            if task_id in visited:
                return
            visiting.add(task_id)
            for dependency in self.steps[task_id].dependencies:
                visit(str(dependency))
            visiting.remove(task_id)
            visited.add(task_id)

        for task_id in self.steps:
            visit(task_id)
