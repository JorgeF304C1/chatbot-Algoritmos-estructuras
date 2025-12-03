from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

from ..datastructures.linked_stack import LinkedStack


class LogService:
    """Stores interaction history using a stack."""

    def __init__(self, max_entries: int = 50):
        self._stack: LinkedStack[str] = LinkedStack()
        self._max_entries = max_entries

    def add_entry(self, label: str, payload: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] {label}: {payload}"
        self._stack.push(message)
        self._enforce_limit()
        return message

    def _enforce_limit(self) -> None:
        if len(self._stack) <= self._max_entries:
            return
        buffer = list(self._stack)
        buffer = buffer[: self._max_entries]
        self._stack.clear()
        for value in reversed(buffer):
            self._stack.push(value)

    def history(self) -> List[str]:
        return list(self._stack)

    def clear(self) -> None:
        self._stack.clear()

    def dump_to_file(self, target: Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as fh:
            for line in reversed(list(self._stack)):
                fh.write(f"{line}\n")
