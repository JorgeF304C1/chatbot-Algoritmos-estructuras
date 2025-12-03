from __future__ import annotations

import re
from typing import List, Tuple


class InputValidator:
    """Normalizes raw user input and extracts command tokens."""

    _prompt_pattern = re.compile(r"^[^:]+:(.*)")

    def sanitize(self, raw: str) -> str:
        text = raw.strip()
        match = self._prompt_pattern.match(text)
        if match:
            text = match.group(1).strip()
        return text.lower()

    def extract_command(self, sanitized: str) -> Tuple[str, List[str]]:
        if not sanitized:
            raise ValueError("Debe ingresar un comando")
        tokens = sanitized.split()
        return tokens[0], tokens[1:]
