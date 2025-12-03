from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from ..datastructures.linked_queue import LinkedQueue


class BackupService:
    """Queues filesystem snapshots and writes them to disk."""

    def __init__(self, backup_dir: str):
        self._backup_dir = Path(backup_dir)
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        self._queue: LinkedQueue[Dict[str, Any]] = LinkedQueue()

    def queue_snapshot(self, command_name: str, snapshot: Dict[str, Any]) -> None:
        payload = {
            "command": command_name,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "snapshot": snapshot,
        }
        self._queue.enqueue(payload)

    def process(self) -> None:
        while len(self._queue) > 0:
            payload = self._queue.dequeue()
            filename = f"backup_{payload['timestamp'].replace(':', '-')}_{payload['command']}.json"
            target = self._backup_dir / filename
            with target.open("w", encoding="utf-8") as fh:
                json.dump(payload, fh, indent=2, ensure_ascii=False)
