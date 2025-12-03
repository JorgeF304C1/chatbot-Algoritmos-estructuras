from __future__ import annotations

from typing import List

from .base import Command, CommandContext


class DirCommand:
    name = "dir"

    def execute(self, args: List[str], context: CommandContext) -> str:
        target = args[0] if args else f"/{context.filesystem.root_name}"
        listing = context.filesystem.list_directory(target)
        lines = [f"Contenido de {target}:"]
        if listing["folders"]:
            lines.append("Carpetas:")
            lines.extend(f"  - {folder}" for folder in listing["folders"])
        if listing["files"]:
            lines.append("Archivos:")
            lines.extend(f"  - {file}" for file in listing["files"])
        if len(lines) == 1:
            lines.append("(vacío)")
        message = "\n".join(lines)
        context.logger.add_entry("dir", message)
        return message
