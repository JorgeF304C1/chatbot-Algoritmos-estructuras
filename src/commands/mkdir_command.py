from __future__ import annotations

from typing import List

from .base import Command, CommandContext


class MkdirCommand:
    name = "mkdir"

    def execute(self, args: List[str], context: CommandContext) -> str:
        if not args:
            raise ValueError("Debe indicar la carpeta a crear")
        created = context.filesystem.make_directory(args[0])
        message = f"Carpeta '{created}' creada correctamente"
        context.logger.add_entry("mkdir", message)
        return message
