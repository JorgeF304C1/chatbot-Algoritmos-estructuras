from __future__ import annotations

from typing import List

from .base import Command, CommandContext


class RmdirCommand:
    name = "rmdir"

    def execute(self, args: List[str], context: CommandContext) -> str:
        if not args:
            raise ValueError("Debe indicar la carpeta a eliminar")
        deleted = context.filesystem.remove_directory(args[0])
        message = f"Carpeta '{deleted}' eliminada correctamente"
        context.logger.add_entry("rmdir", message)
        return message
