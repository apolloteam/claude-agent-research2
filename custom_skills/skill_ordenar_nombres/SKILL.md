---
name: skill-ordenar-nombres
description: Recibe una lista de nombres y la ordena alfabéticamente usando Python. Soporta orden ascendente y descendente, y puede ignorar tildes para el ordenamiento.
---

# Skill: Ordenar Nombres

## ¿Qué hace este skill?

Toma una lista de nombres proporcionada por el usuario y la ordena alfabéticamente
usando el script `scripts/ordenar.py`. Devuelve la lista ordenada con un resumen.

## Cómo usarlo

Cuando el usuario proporcione una lista de nombres para ordenar:

1. Identificá los nombres de la lista (separados por comas, saltos de línea, o numerados)
2. Determiná el orden solicitado: **ascendente** (A→Z, por defecto) o **descendente** (Z→A)
3. Ejecutá el script `ordenar.py` pasando los parámetros correctos
4. Mostrá el resultado ordenado de forma clara

## Parámetros del script

Ver `REFERENCE.md` para documentación completa del script.

## Reglas importantes

- Si la lista está vacía, informar al usuario
- Los nombres con tildes se ordenan correctamente (ej: "Ángel" va con la A, no al final)
- El script devuelve JSON — siempre parsear antes de mostrar al usuario
- Si hay duplicados, mantenerlos (no eliminar)

## Ejemplo de uso

**Usuario:** "Ordená esta lista: Carlos, Ana, Beatriz, Ángel, David"

**Lo que hacés:**
1. Ejecutás `ordenar.py` con esos nombres
2. Mostrás el resultado ordenado: Ángel, Ana, Beatriz, Carlos, David
3. Indicás cuántos nombres había en total
