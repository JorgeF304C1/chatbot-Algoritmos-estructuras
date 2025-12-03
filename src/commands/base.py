from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Protocol

from ..services.backup_service import BackupService
from ..services.log_service import LogService
from ..services.virtual_fs import VirtualFileSystem


@dataclass
class CommandContext:
    filesystem: VirtualFileSystem
    logger: LogService
    backup: BackupService
    settings: Dict

    def should_backup(self, command_name: str) -> bool:
        commands = self.settings.get("auto_backup_commands", [])
        return command_name in commands


class Command(Protocol):
    name: str

    def execute(self, args: List[str], context: CommandContext) -> str:
        ...


class CommandRegistry:
    def __init__(self):
        self._commands: Dict[str, Command] = {}

    def register(self, command: Command) -> None:
        self._commands[command.name] = command

    def get(self, name: str) -> Command:
        if name not in self._commands:
            raise KeyError(f"Comando desconocido: {name}")
        return self._commands[name]

    def available(self) -> List[str]:
        return sorted(self._commands.keys())
