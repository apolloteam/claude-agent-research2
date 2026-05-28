"""
skills_update.py — Actualiza un skill custom en Anthropic con una nueva versión.

Uso:
    python skills_update.py <skill_id> <path>

Ejemplo:
    python skills_update.py skill_0138MRHWJ1YQCbxVU4ccUQAw custom_skills/skill_ordenar_nombres
"""

import sys
from pathlib import Path

import skills_manager


def main():
    if len(sys.argv) != 3:
        print("Uso: python skills_update.py <skill_id> <path>")
        sys.exit(1)

    skill_id = sys.argv[1]
    path = Path(sys.argv[2])

    if not path.exists():
        print(f"Error: path no encontrado: {path}")
        sys.exit(1)

    skills_manager.actualizar_skill(skill_id, path)


if __name__ == "__main__":
    main()
