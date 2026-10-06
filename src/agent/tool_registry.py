"""Central registry for tools available to the agent."""
from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field


class ToolSpec(BaseModel):
    name: str
    description: str
    module_path: str
    timeout_seconds: int = 30
    max_retries: int = 1
    risk_level: str = "low"


class ToolRegistry:
    def __init__(self, tools: List[ToolSpec] | None = None):
        self._tools: Dict[str, ToolSpec] = {tool.name: tool for tool in tools or []}

    def register(self, tool: ToolSpec) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)

    def names(self) -> List[str]:
        return sorted(self._tools)

    def describe(self) -> List[ToolSpec]:
        return list(self._tools.values())


def default_tool_registry(use_enhanced: bool = True) -> ToolRegistry:
    search_module = (
        "src.tools.search_tool_enhanced"
        if use_enhanced
        else "src.tools.search_tool"
    )
    scraper_module = (
        "src.tools.scraper_tool_enhanced"
        if use_enhanced
        else "src.tools.scraper_tool"
    )

    return ToolRegistry(
        [
            ToolSpec(
                name="search",
                description="Search the web for current information.",
                module_path=search_module,
            ),
            ToolSpec(
                name="scrape",
                description="Fetch and extract readable content from web pages.",
                module_path=scraper_module,
            ),
            ToolSpec(
                name="summarize",
                description="Create a concise summary from supplied content.",
                module_path="src.tools.summarizer_tool",
            ),
            ToolSpec(
                name="summarise",
                description="Alias for the summarize capability.",
                module_path="src.tools.summarizer_tool",
            ),
            ToolSpec(
                name="email",
                description="Send or explicitly simulate an email result.",
                module_path="src.tools.email_tool",
                risk_level="medium",
            ),
            ToolSpec(
                name="logger",
                description="Write an execution note to the configured logger.",
                module_path="src.tools.logger_tool",
            ),
            ToolSpec(
                name="resume_parser",
                description="Extract text and fields from a resume file.",
                module_path="src.tools.resume_parser_tool",
            ),
            ToolSpec(
                name="resume_analyzer",
                description="Analyze resume content and identify skills.",
                module_path="src.tools.resume_analyzer_tool",
            ),
            ToolSpec(
                name="job_matcher",
                description="Find and rank jobs against a resume analysis.",
                module_path="src.tools.job_matcher_tool",
            ),
        ]
    )
