# Referencia Técnica: ordenar.py

## Descripción

Script Python que recibe una lista de nombres y los ordena alfabéticamente,
con soporte correcto para caracteres con tildes y ñ (locale español).

## Uso

```bash
python ordenar.py --nombres "Carlos,Ana,Beatriz,Ángel" --orden asc
```

## Parámetros

| Parámetro   | Tipo   | Requerido | Default | Descripción |
|-------------|--------|-----------|---------|-------------|
| `--nombres` | string | Sí        | —       | Nombres separados por coma |
| `--orden`   | string | No        | `asc`   | `asc` (A→Z) o `desc` (Z→A) |

## Salida (JSON)

```json
{
  "ordenados": ["Ángel", "Ana", "Beatriz", "Carlos"],
  "total": 4,
  "orden": "asc",
  "duplicados": 0
}
```

## Campos de salida

| Campo        | Tipo    | Descripción                          |
|--------------|---------|--------------------------------------|
| `ordenados`  | array   | Lista de nombres ordenados           |
| `total`      | integer | Cantidad total de nombres            |
| `orden`      | string  | Orden aplicado (`asc` o `desc`)      |
| `duplicados` | integer | Cantidad de nombres duplicados encontrados |

## Manejo de errores

Si `--nombres` está vacío o no se proporciona, el script retorna:

```json
{
  "error": "La lista de nombres está vacía",
  "ordenados": [],
  "total": 0
}
```

## Notas técnicas

- Usa `locale` con `es_ES.UTF-8` para ordenamiento correcto de tildes y ñ
- Fallback a `unicodedata.normalize` si el locale no está disponible
- Trim de espacios en blanco aplicado a cada nombre antes de ordenar
