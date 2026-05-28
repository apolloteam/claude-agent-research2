"""
ordenar.py — Ordena una lista de nombres alfabéticamente.
by: Esteban 1
Uso:
    python ordenar.py --nombres "Carlos,Ana,Beatriz,Ángel" --orden asc

Parte del skill: skill-ordenar-nombres
"""

import argparse
import json
import locale
import unicodedata


def normalizar(nombre: str) -> str:
    """
    Normaliza un nombre para ordenamiento correcto.
    Convierte tildes a su equivalente sin tilde solo para comparar,
    no modifica el nombre original.
    Ej: 'Ángel' → 'angel' para comparación, pero se muestra como 'Ángel'
    """
    return unicodedata.normalize("NFD", nombre).encode("ascii", "ignore").decode("utf-8").lower()


def ordenar_nombres(nombres: list[str], orden: str = "asc") -> dict:
    """
    Ordena una lista de nombres alfabéticamente.

    Args:
        nombres: Lista de nombres a ordenar
        orden: 'asc' para A→Z, 'desc' para Z→A

    Returns:
        Diccionario con resultados
    """
    if not nombres:
        return {
            "error": "La lista de nombres está vacía",
            "ordenados": [],
            "total": 0,
        }

    # Limpiar espacios en blanco
    nombres_limpios = [n.strip() for n in nombres if n.strip()]

    # Intentar usar locale español para ordenamiento nativo
    try:
        locale.setlocale(locale.LC_COLLATE, "es_ES.UTF-8")
        ordenados = sorted(nombres_limpios, key=locale.strxfrm, reverse=(orden == "desc"))
    except locale.Error:
        # Fallback: normalizar para comparación correcta de tildes
        ordenados = sorted(nombres_limpios, key=normalizar, reverse=(orden == "desc"))

    # Contar duplicados
    duplicados = len(nombres_limpios) - len(set(n.lower() for n in nombres_limpios))

    return {
        "ordenados": ordenados,
        "total": len(ordenados),
        "orden": orden,
        "duplicados": duplicados,
    }


def main():
    parser = argparse.ArgumentParser(description="Ordena una lista de nombres alfabéticamente")
    parser.add_argument(
        "--nombres",
        type=str,
        required=True,
        help="Nombres separados por coma",
    )
    parser.add_argument(
        "--orden",
        type=str,
        default="asc",
        choices=["asc", "desc"],
        help="Orden: asc (A→Z) o desc (Z→A)",
    )

    args = parser.parse_args()

    nombres = args.nombres.split(",")
    resultado = ordenar_nombres(nombres, args.orden)

    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
