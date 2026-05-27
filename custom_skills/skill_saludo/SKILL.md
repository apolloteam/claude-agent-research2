---
name: skill-saludo
description: Genera saludos personalizados en distintos idiomas y estilos (formal, informal, festivo).
---

# Skill: Saludo Personalizado

## ¿Qué hace este skill?

Genera saludos personalizados para una persona según el idioma y estilo solicitado.

## Cómo usarlo

Cuando el usuario pida saludar a alguien, identificá:
1. El **nombre** de la persona
2. El **idioma** (español por defecto)
3. El **estilo**: formal, informal o festivo

## Reglas

- Si no se especifica idioma, usá español
- Si no se especifica estilo, usá informal
- Siempre incluí el nombre en el saludo
- El saludo debe ser breve (1-2 oraciones máximo)

## Ejemplos

**Usuario:** "Saludá a Juan de forma formal"
**Respuesta:** "Estimado Juan, es un placer saludarle."

**Usuario:** "Saludo festivo para María en inglés"
**Respuesta:** "Hey María! 🎉 Wishing you an absolutely wonderful day!"
