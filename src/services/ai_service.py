from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Optional, Tuple
from urllib import error, request


@dataclass
class AISettings:
    enabled: bool
    endpoint: str
    model: str
    api_key_env: str
    system_prompt: str
    provider: str


class AIService:
    """Minimal HTTP client for LLM command suggestions."""

    def __init__(self, settings: AISettings):
        self._settings = settings
        self._api_key = os.getenv(settings.api_key_env, "")
        self._last_error: Optional[str] = None
        self._provider = (settings.provider or "openai").lower()

    def is_ready(self) -> bool:
        return (
            self._settings.enabled
            and bool(self._settings.endpoint)
            and bool(self._settings.model)
            and bool(self._api_key)
        )

    def suggest_command(self, user_message: str) -> Optional[str]:
        self._last_error = None
        if not self.is_ready():
            self._last_error = "IA no configurada o sin API key"
            return None
        request_data = self._build_request(user_message)
        if not request_data:
            return None
        url, payload, headers = request_data
        try:
            req = request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = self._extract_content(data)
            if not content:
                self._last_error = "La IA no devolvió contenido"
                return None
            return content.strip()
        except error.HTTPError as http_err:
            detail = http_err.read().decode("utf-8", errors="ignore") if http_err.fp else str(http_err)
            self._last_error = f"HTTP {http_err.code}: {detail.strip()}"
        except Exception as exc:  # pragma: no cover - red/timeout entran aquí
            self._last_error = f"{exc.__class__.__name__}: {exc}"
        return None

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    def _build_request(self, user_message: str) -> Optional[Tuple[str, dict, dict]]:
        prompt = f"Texto del usuario: {user_message}. Devuelve solo el comando a ejecutar."
        if self._provider == "openai":
            payload = {
                "model": self._settings.model,
                "messages": [
                    {"role": "system", "content": self._settings.system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.1,
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            }
            return self._settings.endpoint, payload, headers

        if self._provider == "gemini":
            url = self._settings.endpoint
            if "key=" not in url:
                separator = "&" if "?" in url else "?"
                url = f"{url}{separator}key={self._api_key}"
            payload = {
                "systemInstruction": {
                    "parts": [{"text": self._settings.system_prompt}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}],
                    }
                ],
                "generationConfig": {"temperature": 0.1},
            }
            headers = {"Content-Type": "application/json"}
            return url, payload, headers

        self._last_error = f"Proveedor IA no soportado: {self._provider}"
        return None

    def _extract_content(self, data: dict) -> Optional[str]:
        if self._provider == "openai":
            return data.get("choices", [{}])[0].get("message", {}).get("content")
        if self._provider == "gemini":
            candidates = data.get("candidates") or []
            if not candidates:
                return None
            content = candidates[0].get("content", {})
            parts = content.get("parts") or []
            if not parts:
                return None
            return parts[0].get("text")
        return None
