"""
excel_to_js.py
==============
Lee genealogia_organizada.xlsx y genera genealogia_data.js.

Flujo de actualización:
  1. El usuario edita el Excel (agrega datos, URLs, imágenes, etc.)
  2. Ejecutar este script:  python excel_to_js.py
  3. El genealogia_data.js se regenera automáticamente.

Netlify ejecuta este script en cada deploy.

Columnas del Excel
------------------
Columnas de datos (generadas por organizar_genealogia.py):
  Padre, Madre, Hijos, Orden de Nacimiento, Género Hijos,
  Lugar de nacimiento, Significado del Nombre (Padre),
  Referencia, Información Adicional, Notas

Columnas editables por el usuario:
  Imagen_URL        URL de la imagen/retrato del personaje (cualquier host público,
                    p. ej. Imgur, Google Drive, GitHub raw, etc.)
  Referencias_URLs  URLs de las referencias bíblicas, separadas por | (pipe).
                    Cada URL corresponde por posición a una cita en el campo Referencia.
                    Ejemplo:
                      https://site.com/genesis-1|https://site.com/lucas-3
  Enlace_Externo    URL de una fuente externa de información adicional sobre el personaje.
"""

import json
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas no está instalado. Ejecuta:  pip install pandas openpyxl")
    sys.exit(1)

# ── Configuración ─────────────────────────────────────────────────────────────
EXCEL_INPUT = "genealogia_organizada.xlsx"
JS_OUTPUT   = "genealogia_data.js"

# Columnas que deben existir en el Excel.
# Las columnas editables se añaden vacías si no existen.
REQUIRED_EDITABLE_COLS = ["Imagen_URL", "Referencias_URLs", "Enlace_Externo"]

# Orden final de columnas en el JS (para que el frontend sea predecible)
COLUMN_ORDER = [
    "Padre", "Madre", "Hijos", "Orden de Nacimiento", "Género Hijos",
    "Lugar de nacimiento", "Significado del Nombre (Padre)",
    "Referencia", "Información Adicional", "Notas",
    "Imagen_URL", "Referencias_URLs", "Enlace_Externo",
]
# ──────────────────────────────────────────────────────────────────────────────


def load_excel(path: str) -> pd.DataFrame:
    """Lee el Excel y garantiza que existen todas las columnas necesarias."""
    print(f"Leyendo {path}...")
    df = pd.read_excel(path, dtype=str)

    # Añadir columnas editables vacías si no existen todavía
    for col in REQUIRED_EDITABLE_COLS:
        if col not in df.columns:
            df[col] = ""
            print(f"  + Columna '{col}' anadida (vacia).")

    # Reordenar columnas: primero las conocidas, luego cualquier extra
    extra_cols = [c for c in df.columns if c not in COLUMN_ORDER]
    ordered = [c for c in COLUMN_ORDER if c in df.columns] + extra_cols
    df = df[ordered]

    # Reemplazar NaN por cadena vacía para que el JSON sea limpio
    df = df.fillna("")

    return df


def df_to_records(df: pd.DataFrame) -> list[dict]:
    """Convierte el DataFrame a lista de dicts limpia."""
    records = df.to_dict(orient="records")
    # Asegurar que todos los valores son strings o números (no float NaN)
    clean = []
    for row in records:
        clean_row = {}
        for k, v in row.items():
            if v is None or (isinstance(v, float) and str(v) == "nan"):
                clean_row[k] = ""
            else:
                clean_row[k] = str(v).strip() if isinstance(v, str) else v
        clean.append(clean_row)
    return clean


def write_js(records: list[dict], path: str):
    """Escribe el archivo JS con la constante GENEALOGIA_DATA."""
    js_content = (
        "// genealogia_data.js — generado automáticamente por excel_to_js.py\n"
        "// NO editar este archivo directamente; editar genealogia_organizada.xlsx\n"
        f"const GENEALOGIA_DATA = {json.dumps(records, ensure_ascii=False, indent=2)};\n"
    )
    Path(path).write_text(js_content, encoding="utf-8")
    print(f"OK {path} generado con {len(records)} registros.")


def save_excel_with_new_cols(df: pd.DataFrame, path: str):
    """
    Sobreescribe el Excel si se añadieron columnas nuevas,
    para que el usuario las vea al abrirlo.
    """
    df.to_excel(path, index=False)
    print(f"OK {path} actualizado con las nuevas columnas.")


def main():
    if not Path(EXCEL_INPUT).exists():
        print(f"ERROR: No se encontró '{EXCEL_INPUT}' en el directorio actual.")
        sys.exit(1)

    df = load_excel(EXCEL_INPUT)

    # Si se añadieron columnas nuevas, guardamos el Excel actualizado
    cols_in_file = list(pd.read_excel(EXCEL_INPUT, nrows=0).columns)
    new_cols_added = any(c not in cols_in_file for c in REQUIRED_EDITABLE_COLS)
    if new_cols_added:
        save_excel_with_new_cols(df, EXCEL_INPUT)

    records = df_to_records(df)
    write_js(records, JS_OUTPUT)
    print(f"\nListo. Abre {JS_OUTPUT} o los archivos HTML para ver los cambios.")


if __name__ == "__main__":
    main()
