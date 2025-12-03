# Proyecto: Chatbot de Pilas y Colas

Implementación orientada a objetos que simula un chatbot de consola para gestionar un árbol de directorios usando estructuras TDA de Pilas y Colas basadas en listas enlazadas.

## Integrantes
- Steven Alcalá — CI 31.542.054
- Jorge Fattal — CI 31.505.044
- Ricardo Elbazi — CI 31.541.609

## Requisitos cubiertos
- Paradigma orientado a objetos: clases `ChatbotShell`, servicios y comandos.
- Pilas y colas enlazadas (`LinkedStack`, `LinkedQueue`).
- Validación de entradas vía `InputValidator` y excepciones controladas.
- Datos por defecto (`data/default_fs.json`, `data/sample_inputs.txt`).

## Estructura inicial
- `src/` código fuente principal.
- `config/settings.json` configuración base.
- `data/default_fs.json` estructura de archivos inicial.
- `data/backups/` salidas de respaldo.
- `tests/` (pendiente) casos automatizados.

## Uso rápido
```bash
python -m src.main
```
Escribe comandos como `dir /Documentos`, `rmdir /Documentos/Fotos`, `clear`, `log 5` o `salir`.

### Comando listo para demo en PowerShell
Reemplaza `TU_API_KEY` con tu clave real antes de pegarlo en la terminal del laboratorio:
```powershell
$Env:GEMINI_API_KEY="AIzaSyBwH3Gvp6VXc1pNSu3kpmP5qTaVYMkgXdA"; python -m src.main
```
Si usas otro proveedor (por ejemplo `openai`), basta con cambiar el nombre de la variable para que coincida con `ai.api_key_env`.

## Integración con IA (opcional)
- Define la variable de entorno indicada en `ai.api_key_env` (por ejemplo `AI_API_KEY` u `GEMINI_API_KEY`) con tu token del proveedor configurado.
- Ajusta `config/settings.json` → bloque `ai` (`enabled`, `provider`, `endpoint`, `model`, `system_prompt`).
- `provider` soporta `openai` (Chat Completions compatibles) y `gemini` (Google Generative Language). Usa `AI_API_KEY` u otra variable como `GEMINI_API_KEY` según corresponda.
- Al estar habilitado, mensajes ambiguos se envían a un LLM que responde con un comando concreto (`dir`, `rmdir`, `log`, `clear`).
- Cada sugerencia aceptada queda registrada en el historial bajo la etiqueta `ai`.

## Próximos pasos
1. Ampliar comandos (`mkdir`, `search`).
2. Persistir historial en disco usando `LogService.dump_to_file`.
3. Agregar pruebas unitarias (ver sección Tests pendiente).

## Tests
Ejecuta `pytest` en la raíz del proyecto para validar las estructuras de datos y el filesystem virtual (`tests/test_datastructures.py`).
