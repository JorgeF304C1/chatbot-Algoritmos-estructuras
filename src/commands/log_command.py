from __future__ import annotations

from typing import List

from .base import Command, CommandContext


class LogCommand:
    name = "log"

    def execute(self, args: List[str], context: CommandContext) -> str:
        limit = None
        if args:
            try:
                limit = max(1, int(args[0]))
            except ValueError as exc:
                raise ValueError("El parámetro de log debe ser numérico") from exc
        entries = context.logger.history()
        if not entries:
            return "No hay entradas en el historial"
        if limit:
            entries = entries[:limit]
        lines = ["Historial reciente:"]
        lines.extend(entries)
        return "\n".join(lines)
