from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class ConfigLoader:
    """Loads JSON settings and provides dictionary-style access."""

    def __init__(self, config_path: str):
        self._path = Path(config_path)
        if not self._path.exists():
            raise FileNotFoundError(f"No se encontró la configuración: {config_path}")
        with self._path.open("r", encoding="utf-8") as fh:
            self._data: Dict[str, Any] = json.load(fh)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    def resolve_path(self, relative: str) -> Path:
        base = self._path.parent
        return (base.parent / relative).resolve()
