# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Propósito

Proyecto de investigación que demuestra cómo construir un agente Claude con skills custom, prompt caching y ejecución de código Python. Combina un skill built-in de Anthropic (PDF) con dos skills custom definidos en `custom_skills/`.

## Setup y ejecución

```bash
pip install anthropic python-dotenv
cp .env.example .env
# Editar .env y agregar ANTHROPIC_API_KEY
```

Registrar los skills custom **una sola vez** y copiar los IDs resultantes a `agente.py`:

```bash
python skills_manager.py
```

Correr el agente interactivo:

```bash
python agente.py
```

No hay test runner ni linter configurado.

## Arquitectura

### Flujo principal

`agente.py` implementa un loop conversacional que:
1. Acumula el historial completo de mensajes turno a turno.
2. Envía cada turno a `client.beta.messages.create` con los 3 skills + `code_execution` tool.
3. Concatena los bloques con `.text` de la respuesta (puede haber bloques sin texto cuando se ejecutan tools/skills).
4. Reporta el uso de tokens por turno (cache_write / cache_read / input / output).

### Prompt caching

El system prompt lleva `cache_control: ephemeral`. Desde el turno 2, el system prompt se lee del cache (~10% del costo normal). El historial del asistente tiene la lógica de caching comentada (`limpiar_cache_viejo` existe pero no se llama) para simplificar el ejemplo.

### Skills

Cada skill custom vive en `custom_skills/<nombre>/` con esta convención:

| Archivo | Cuándo lo carga Claude | Para qué |
|---|---|---|
| `SKILL.md` | Cuando decide usar el skill | Instrucciones de uso |
| `REFERENCE.md` | Cuando necesita detalles técnicos | Parámetros, salidas, errores |
| `scripts/*.py` | Durante la ejecución | Código que corre el agente |
| `resources/` | Si Claude lo necesita | Datos de prueba / recursos |

`skills_manager.py` expone cuatro operaciones sobre la API beta de Anthropic: `registrar_skills`, `listar_skills`, `actualizar_skill`, `eliminar_skill`.

### Betas requeridos

```
anthropic-beta: code-execution-2025-08-25,files-api-2025-04-14,skills-2025-10-02
```

Se configuran en el cliente de `agente.py` vía `default_headers`. El cliente de `skills_manager.py` no necesita estos headers (solo gestiona el registro de skills).

## Git Commits
- Usar el estándar Conventional Commits para todos los mensajes de commit.
  - Formato: `<tipo>[scope opcional]: <descripción>`.
  - Tipos permitidos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`.
  - La descripción en minúsculas y en español.
  - Si el cambio rompe compatibilidad, agregar `!` antes de `:` o footer `BREAKING CHANGE:`.
  - Usar verbo en tercera persona del singular (presente indicativo) en la descripción, no infinitivo.
    La descripción debe completar la frase "Si se aplica, este commit..."
    ✓ "feat: agrega validación de email"
    ✗ "feat: agregar validación de email"
- Siempre mostrar el mensaje del commit propuesto y esperar confirmación antes de ejecutarlo.
- NUNCA agregar trailers al commit (ni "Co-Authored-By", ni "Generated-by", ni ningún footer automático).
  
## Notas críticas

- Los IDs de los skills están hardcodeados en `agente.py` (líneas 71–72). Si se re-registran los skills, los IDs cambian y hay que actualizarlos.
- Los skills quedan asociados a la API key hasta que se eliminen explícitamente con `eliminar_skill`.
- La respuesta de la API puede contener bloques sin `.text` (`ToolUseBlock`, `ToolResultBlock`); el loop en `agente.py` ya filtra por `hasattr(block, "text")`.
