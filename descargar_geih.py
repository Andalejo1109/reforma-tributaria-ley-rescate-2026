"""Descarga los microdatos GEIH 2026 (ene-ago) del catálogo DANE 900 y extrae solo el módulo 'Ocupados'.
Uso: python descargar_geih.py   -> crea geih/x1..x8/Ocupados.csv  (no se versionan; ver .gitignore)
Fuente: https://microdatos.dane.gov.co/index.php/catalog/900/get-microdata
Si un enlace cambia, descarga el ZIP del mes manualmente desde esa página y descomprime 'Ocupados.CSV' en geih/xN/.
"""
import os, zipfile, urllib.request
IDS = [24530, 24594, 24674, 24703, 24731, 24760, 24791, 24811]  # Enero..Agosto 2026
os.makedirs("geih", exist_ok=True)
for i, rid in enumerate(IDS, start=1):
    z = f"geih/m{i}.zip"
    if not os.path.exists(z):
        url = f"https://microdatos.dane.gov.co/index.php/catalog/900/download/{rid}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as r, open(z, "wb") as f:
            f.write(r.read())
    os.makedirs(f"geih/x{i}", exist_ok=True)
    with zipfile.ZipFile(z) as zf:
        for n in zf.namelist():
            base = os.path.basename(n)
            if n.lower().startswith("csv/") and base.lower() == "ocupados.csv":
                with zf.open(n) as src, open(f"geih/x{i}/Ocupados.csv", "wb") as dst:
                    dst.write(src.read())
    print("ok mes", i)
