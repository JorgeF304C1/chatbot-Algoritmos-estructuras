from __future__ import annotations

import sys
from pathlib import Path

from .services.chatbot_shell import ChatbotShell


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "config" / "settings.json"
    shell = ChatbotShell(str(config_path))
    print("Chatbot de Pilas y Colas listo. Escriba 'salir' para terminar.")
    print(f"Comandos disponibles: {', '.join(shell.available_commands())}")
    while True:
        try:
            raw = input("C:!> Usuario: ")
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego")
            break
        if raw.strip().lower() in {"salir", "exit"}:
            print("Fin de la sesión")
            break
        response = shell.process_message(raw)
        print(f"Cortana: {response}")


if __name__ == "__main__":
    main()
