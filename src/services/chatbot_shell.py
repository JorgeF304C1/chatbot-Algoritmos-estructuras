from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Tuple

from ..commands.base import CommandContext, CommandRegistry
from ..commands.clear_log_command import ClearLogCommand
from ..commands.dir_command import DirCommand
from ..commands.log_command import LogCommand
from ..commands.rmdir_command import RmdirCommand
from .ai_service import AIService, AISettings
from .backup_service import BackupService
from .config_loader import ConfigLoader
from .input_validator import InputValidator
from .log_service import LogService
from .virtual_fs import VirtualFileSystem


class ChatbotShell:
    """High-level orchestrator that parses user messages and triggers commands."""

    def __init__(self, config_path: str):
        self._config = ConfigLoader(config_path)
        self._validator = InputValidator()
        self._filesystem = self._load_filesystem()
        self._logger = LogService(max_entries=self._config.get("max_log_entries", 50))
        backup_dir = self._config.resolve_path(self._config.get("backup_dir"))
        self._backup = BackupService(str(backup_dir))
        self._ai = self._build_ai_service()
        self._registry = CommandRegistry()
        self._context = CommandContext(
            filesystem=self._filesystem,
            logger=self._logger,
            backup=self._backup,
            settings=self._config.data,
        )
        self._register_commands()
        self._prime_defaults()

    def _load_filesystem(self) -> VirtualFileSystem:
        seed_path = self._config.resolve_path(self._config.get("filesystem_seed"))
        with Path(seed_path).open("r", encoding="utf-8") as fh:
            seed = json.load(fh)
        return VirtualFileSystem.from_seed(seed)

    def _register_commands(self) -> None:
        self._registry.register(DirCommand())
        self._registry.register(RmdirCommand())
        self._registry.register(ClearLogCommand())
        self._registry.register(LogCommand())

    def _prime_defaults(self) -> None:
        for command in self._config.get("default_commands", []):
            self.process_message(command)

    def process_message(self, raw_message: str) -> str:
        ai_result: Optional[Tuple[str, List[str]]] = None
        try:
            sanitized = self._validator.sanitize(raw_message)
            command_name, args = self._validator.extract_command(sanitized)
        except ValueError as parse_error:
            ai_result = self._ai_interpret(raw_message)
            if not ai_result:
                extra = self._ai.last_error
                message = str(parse_error)
                if extra:
                    message = f"{message}. Detalle IA: {extra}"
                self._logger.add_entry("error", message)
                return f"Error: {message}"
            command_name, args = ai_result

        try:
            command = self._registry.get(command_name)
        except KeyError as lookup_error:
            if not ai_result:
                ai_result = self._ai_interpret(raw_message)
            if not ai_result:
                extra = self._ai.last_error
                message = str(lookup_error)
                if extra:
                    message = f"{message}. Detalle IA: {extra}"
                self._logger.add_entry("error", message)
                return f"Error: {message}"
            command_name, args = ai_result
            try:
                command = self._registry.get(command_name)
            except KeyError as final_error:
                extra = self._ai.last_error
                message = str(final_error)
                if extra:
                    message = f"{message}. Detalle IA: {extra}"
                self._logger.add_entry("error", message)
                return f"Error: {message}"

        result = command.execute(args, self._context)
        if self._context.should_backup(command_name):
            self._backup.queue_snapshot(command_name, self._filesystem.snapshot())
            self._backup.process()
        return result

    def available_commands(self) -> List[str]:
        return self._registry.available()

    @property
    def history(self) -> List[str]:
        return self._logger.history()

    def _build_ai_service(self) -> AIService:
        ai_config = self._config.get("ai", {}) or {}
        settings = AISettings(
            enabled=ai_config.get("enabled", False),
            endpoint=ai_config.get("endpoint", ""),
            model=ai_config.get("model", ""),
            api_key_env=ai_config.get("api_key_env", ""),
            system_prompt=ai_config.get(
                "system_prompt",
                "Eres un asistente que traduce frases a comandos dir/rmdir/log/clear",
            ),
            provider=ai_config.get("provider", "openai"),
        )
        return AIService(settings)

    def _ai_interpret(self, raw_message: str) -> Optional[Tuple[str, List[str]]]:
        if not self._ai.is_ready():
            return None
        suggestion = self._ai.suggest_command(raw_message)
        if not suggestion:
            if self._ai.last_error:
                self._logger.add_entry("ai-error", self._ai.last_error)
            return None
        try:
            sanitized = self._validator.sanitize(suggestion)
            command_name, args = self._validator.extract_command(sanitized)
        except ValueError:
            return None
        self._logger.add_entry(
            "ai", f"Entrada '{raw_message}' interpretada como '{suggestion}'"
        )
        return command_name, args
