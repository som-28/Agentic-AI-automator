"""Simple file-backed memory/context manager.

Stores contexts in a JSON file and provides basic read/write operations.
"""
import json
from pathlib import Path
from typing import Any


class Memory:
    def __init__(self, path: str | None = None):
        self.path = Path(path or "agent_memory.json")
        if not self.path.exists():
            self._write({})

    def _read(self) -> dict:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _write(self, data: dict):
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get(self, key: str, default: Any = None) -> Any:
        data = self._read()
        return data.get(key, default)

    def set(self, key: str, value: Any):
        data = self._read()
        data[key] = value
        self._write(data)

    def clear(self):
        self._write({})
