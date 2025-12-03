from __future__ import annotations

from typing import List

from .base import Command, CommandContext


class ClearLogCommand:
    name = "clear"

    def execute(self, args: List[str], context: CommandContext) -> str:
        context.logger.clear()
        return "Historial limpiado"
