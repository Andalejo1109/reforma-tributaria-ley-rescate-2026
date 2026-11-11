"""Genera output/carga_por_nivel_ingreso.png a partir de resultados.csv (ejecutar después de calc.py)."""
import os, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
r = pd.read_csv("resultados.csv")
x = [f"{int(m/1e6)}M" for m in r.ingreso_mensual]
os.makedirs("output", exist_ok=True)
fig, ax = plt.subplots(figsize=(9,5.2))
w = 0.2; idx = range(len(x))
series = [("Δ renta", r["delta_renta_%ing"]), ("IVA mercado fijo $500k", r["ivaA_500k_tras100_%ing"]),
          ("IVA mercado creciente", r["ivaB_tras100_%ing"]), ("Δ salud (cotización)", r["delta_salud_%ing"])]
for k,(lab,s) in enumerate(series):
    ax.bar([i+(k-1.5)*w for i in idx], s, w, label=lab)
ax.plot(list(idx), r["total_renta+ivaB_%ing"], "ko-", label="Total renta + IVA (creciente)")
ax.plot(list(idx), r["total_renta+salud+ivaB_%ing"], "s--", color="crimson", label="Total renta + salud + IVA")
ax.set_xticks(list(idx)); ax.set_xticklabels(x); ax.set_xlabel("Ingreso laboral mensual (COP)")
ax.set_ylabel("% del ingreso mensual")
ax.set_title("Ley de Rescate Económico (PL 477/2026 C): carga incremental por nivel de ingreso\nEjercicio estático, parámetros 2026, traslado total del IVA. Educativo.")
ax.legend(fontsize=8); ax.grid(axis="y", alpha=.3)
fig.tight_layout(); fig.savefig("output/carga_por_nivel_ingreso.png", dpi=150)
print("output/carga_por_nivel_ingreso.png")
