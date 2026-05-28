import os
from pathlib import Path

import anthropic
from anthropic.lib import files_from_dir
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

SKILLS_DIR = Path(__file__).parent / "custom_skills"


def registrar_skills():
    """
    Registra todos los skills custom — UNA SOLA VEZ.
    TODO: Copiar los IDs a agente.py.
    """
    
    print("📤 Registrando skills custom...\n")

    skills_a_registrar = [
        SKILLS_DIR / "skill_saludo",
        SKILLS_DIR / "skill_ordenar_nombres",
    ]

    for path in skills_a_registrar:
        registrar_skill(path)


def registrar_skill(path: Path) -> str | None:
    """
    Sube un skill custom a Anthropic y devuelve su ID.
    Toma el nombre del directorio indicado en path.
    En producción esto se hace una sola vez y se guarda el ID.
    """
    if not path.exists():
        print(f"  ❌ Path no encontrado: {path}")
        return None

    nombre = path.name
    display_title = nombre.replace("_", " ").title()

    print(f"  Subiendo: {nombre} desde {path}")
    skill = client.beta.skills.create(
        display_title=display_title,
        files=files_from_dir(str(path)),
    )
    print(f"  ✅ Registrado → ID: {skill.id} | Path: {path}\n")
    return skill.id


def listar_skills():
    """Lista todos los skills custom registrados en tu cuenta."""
    skills = client.beta.skills.list(source="custom")
    print("\n📋 Skills custom registrados:")
    for s in skills.data:
        print(f"  • {s.display_title} → ID: {s.id} (v{s.latest_version})")
    print()


def actualizar_skill(skill_id: str, nueva_version_path: Path):
    """Actualiza un skill custom subiendo una nueva versión."""
    print(f"🔄 Actualizando skill {skill_id} con nueva versión desde {nueva_version_path}")
    nueva_version = client.beta.skills.versions.create(
        skill_id=skill_id,
        files=files_from_dir(str(nueva_version_path)),
    )
    print(f"  ✅ Nueva versión creada → v{nueva_version.version}\n")  


def eliminar_skill(skill_id: str):
    """Elimina un skill custom por ID."""
    versions = client.beta.skills.versions.list(skill_id=skill_id)
    for v in versions.data:
        client.beta.skills.versions.delete(skill_id=skill_id, version=v.version)
    client.beta.skills.delete(skill_id)
    print(f"  🗑️  Skill {skill_id} eliminado")


if __name__ == "__main__":
    #registrar_skills()

    # Opcional: listar skills registrados
    # listar_skills()

    # Opcional: limpiar los skills creados en este ejemplo
    # listar_skills()  # obtener los IDs primero
    # eliminar_skill("<skill_id>")
