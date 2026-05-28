"""
agente.py — Ejemplo completo de agente con skills personalizados.

# ⚠ IMPORTANTE: Requiere tener registrados los skills custom en Anthropic y usar sus IDs aquí.
# Si no estan registrados, registrarlos usando skills_manager.py y copiar los IDs resultantes.

Skills usados:
  1. PDF (Anthropic built-in)        → genera PDFs
  2. skill-saludo (custom simple)    → saludos personalizados
  3. skill-ordenar-nombres (custom)  → ordena listas con script Python

Temas cubiertos:
  - Registro de skills custom
  - Loop de conversación con historial
  - Prompt caching (system prompt + historial)
  - Tokens por turno
"""

import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────────

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    default_headers={
        # Betas requeridos para skills + code execution + files API
        "anthropic-beta": "code-execution-2025-08-25,files-api-2025-04-14,skills-2025-10-02"
    },
)

MODEL = "claude-sonnet-4-6"

# System prompt (simulamos uno grande de ~10.000 tokens en producción)
SYSTEM_PROMPT = """
Eres un asistente multifuncional con acceso a skills especializados.

Tenés disponibles los siguientes skills:
- PDF: para generar documentos PDF
- Saludo personalizado: para generar saludos en distintos idiomas y estilos
- Ordenar nombres: para ordenar listas de nombres alfabéticamente usando Python

Reglas generales:
- Respondé siempre en español
- Sé conciso y claro
- Si el usuario pide algo que requiere un skill, usalo
- Indicá siempre qué skill estás usando

Para finalizar la conversación el usuario puede escribir: "finalizar chat"
""".strip()

# ─────────────────────────────────────────────
# Paso 1: Loop del agente
# ─────────────────────────────────────────────

def correr_agente():
    """
    Loop principal del agente con:
    - 3 skills (1 Anthropic + 2 custom)
    - Historial de conversación completo
    - Prompt caching en system prompt e historial
    - Reporte de tokens por turno
    """

    skill_id_saludo = os.getenv("SKILL_ID_SALUDO")
    skill_id_ordenar_nombres = os.getenv("SKILL_ID_ORDENAR_NOMBRES")

    # Configuración de los 3 skills
    skills_config = [
        # 1. Skill de Anthropic (built-in)
        {"type": "anthropic", "skill_id": "pdf", "version": "latest"},

        # 2. Skill custom simple (saludo)
        {"type": "custom", "skill_id": skill_id_saludo, "version": "latest"},

        # 3. Skill custom con script (ordenar nombres)
        {"type": "custom", "skill_id": skill_id_ordenar_nombres, "version": "latest"},
    ]

    # Historial vacío al inicio — crecerá turno a turno
    messages = []

    print("=" * 60)
    print("🤖 Agente iniciado con 3 skills:")
    print("   • PDF (Anthropic built-in)")
    print("   • Saludo personalizado (custom simple)")
    print("   • Ordenar nombres (custom con script Python)")
    print("\nEscribí 'finalizar chat' para terminar.")
    print("=" * 60 + "\n")

    while True:
        user_input = input("Vos: ").strip()
        if not user_input:
            continue

        # Agregamos el mensaje del usuario al historial
        messages.append({"role": "user", "content": user_input})

        # Limpiamos marcas de cache_control de mensajes anteriores (si las hay).
        # NOTA: En messages.append más abajo, comente la línea que le pone la marca de chache para simplicidad en este ejemplo.
        #messages = limpiar_cache_viejo(messages)

        if user_input.lower() == "finalizar chat":
            print("\nAsistente: ¡Hasta luego! 👋")
            break

        # ── Llamada a la API ──────────────────────────────────────
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=2048,

            # System prompt con cache (siempre igual → siempre hit desde turno 2)
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},  # marca 1
                }
            ],

            # Historial completo con cache en el último mensaje del asistente
            messages=messages,

            # Los 3 skills
            container={"skills": skills_config},

            # Necesario para que los skills puedan ejecutar código
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        )
        # ─────────────────────────────────────────────────────────

        # Extraer respuesta de texto.
        # NOTA: Al usar tolls/skills, la respuesta puede venir sin la propiedad "text". Ejemplo:
        # [
        #     TextBlock(text="Voy a ordenar la lista..."),       # ← tiene .text ✅
        #     ToolUseBlock(name="code_execution", input={...}),  # ← NO tiene .text ❌
        #     ToolResultBlock(output="[...]"),                   # ← NO tiene .text ❌
        #     TextBlock(text="Aquí está la lista ordenada: ...") # ← tiene .text ✅
        # ]
        assistant_reply = ""
        for block in response.content:
            if hasattr(block, "text"): # solo los bloques que tienen texto
                assistant_reply += block.text # se concatenan

        # Agregar respuesta al historial CON cache en el último mensaje
        # Esto cachea todo el historial hasta este punto para el próximo turno.
        # NOTA: Para este ejemplo no ponemos cache_control en el último mensaje ya
        # que si se hace hay que crear otra función que limpie todos los anteriores
        # (en messages) ya que solo se permiten 4.
        messages.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": assistant_reply,
                    #"cache_control": {"type": "ephemeral"},  # marca 2 (se mueve cada turno)
                }
            ],
        })

        print(f"\nAsistente: {assistant_reply}\n")

        # Reporte de tokens
        u = response.usage
        print(
            f"[tokens → "
            f"cache_write: {getattr(u, 'cache_creation_input_tokens', 0)} | "
            f"cache_read: {getattr(u, 'cache_read_input_tokens', 0)} | "
            f"input: {u.input_tokens} | "
            f"output: {u.output_tokens}]"
        )
        print()

def limpiar_cache_viejo(messages: list) -> list:
    """
    Elimina cache_control de todos los mensajes del asistente
    excepto el último. Solo el más reciente necesita la marca.
    """
    # Encontrar el índice del último mensaje del asistente
    ultimo_asistente = None
    for i in range(len(messages) - 1, -1, -1):
        if messages[i]["role"] == "assistant":
            ultimo_asistente = i
            break

    # Limpiar cache_control de todos los mensajes del asistente anteriores
    for i, msg in enumerate(messages):
        if msg["role"] == "assistant" and i != ultimo_asistente:
            if isinstance(msg["content"], list):
                for block in msg["content"]:
                    block.pop("cache_control", None)

    return messages

# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Registramos los skills custom
    # En producción harías esto UNA SOLA VEZ y guardarías los IDs
    #skill_ids = registrar_skills()

    # Corremos el agente
    correr_agente()

    # Opcional: listar skills registrados
    # listar_skills()

    # Opcional: limpiar los skills creados en este ejemplo
    # for sid in skill_ids.values():
    #     eliminar_skill(sid)
