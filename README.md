# Ejemplo: Agente con Skills Custom

Ejemplo completo de un agente en Python que combina todo lo visto:
loop de conversación, prompt caching y 3 skills (1 Anthropic + 2 custom).

## Estructura del proyecto

```
skills_ejemplo/
├── agente.py                          # Agente principal
├── .env                               # API key (crear desde .env.example)
├── .env.example
├── requirements.txt
└── custom_skills/
    ├── skill_saludo/
    │   └── SKILL.md                   # Skill simple (solo instrucciones)
    │
    └── skill_ordenar_nombres/
        ├── SKILL.md                   # Instrucciones principales
        ├── REFERENCE.md               # Documentación técnica del script
        ├── scripts/
        │   └── ordenar.py             # Script Python que ejecuta Claude
        └── resources/
            └── nombres_ejemplo.md     # Datos de prueba
```

## Cómo funciona cada archivo de un skill

| Archivo | Cuándo lo carga Claude | Para qué |
|---|---|---|
| `SKILL.md` | Cuando decide usar el skill | Instrucciones de uso |
| `REFERENCE.md` | Cuando necesita detalles técnicos | Parámetros, salidas, errores |
| `scripts/ordenar.py` | Durante la ejecución | Código real que corre |
| `resources/nombres_ejemplo.md` | Si Claude lo necesita | Datos de prueba |

## Setup

```bash
pip install anthropic python-dotenv
cp .env.example .env
# Editá .env y poné tu ANTHROPIC_API_KEY
```

## Correr el agente

```bash
python agente.py
```

## Qué hace el agente

Podés pedirle:
- `"Saludá a María de forma formal"` → usa skill-saludo
- `"Ordená: Carlos, Ana, Beatriz, Ángel"` → usa skill-ordenar-nombres con el script Python
- `"Generá un PDF con el resumen de esta conversación"` → usa skill PDF de Anthropic
- `"finalizar chat"` → termina el loop

## Caching de tokens

Cada turno verás el reporte:
```
[tokens → cache_write: 850 | cache_read: 0 | input: 45 | output: 120]   ← turno 1
[tokens → cache_write: 0   | cache_read: 850 | input: 60 | output: 95]  ← turno 2+
```

Desde el turno 2 el system prompt se lee del cache (~10% del costo normal).

## Notas importantes

- `registrar_skills()` se llama **una sola vez**. En producción guardá los IDs
  en tu `.env` o base de datos para no re-registrar en cada ejecución.
- Los skills custom quedan asociados a tu API key hasta que los eliminés.
- El `cache_control` en el último mensaje del asistente se mueve en cada turno
  para cachear el historial acumulado.
