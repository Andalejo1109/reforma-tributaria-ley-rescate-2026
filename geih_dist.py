"""Distribución del ingreso laboral mensual - GEIH DANE ene-ago 2026 (microdatos, catálogo 900).
Pool de 8 meses; factor de expansión FEX_C18 / 8 (promedio mensual)."""
import pandas as pd, numpy as np, glob
SMMLV = 1_750_905
frames=[]
for i in range(1,9):
    f=glob.glob(f"geih/x{i}/Ocupados.*")[0]
    d=pd.read_csv(f,sep=";",usecols=["MES","FEX_C18","INGLABO","P6430","CLASE"],decimal=",",low_memory=False,encoding="latin-1")
    d["MESF"]=i; frames.append(d)
d=pd.concat(frames)
for c in ["FEX_C18","INGLABO","P6430"]:
    d[c]=pd.to_numeric(d[c].astype(str).str.replace(",","."),errors="coerce")
d["w"]=d.FEX_C18/8
def wq(x,w,q):
    o=np.argsort(x); x=x[o]; w=w[o]; c=np.cumsum(w)/w.sum(); return np.interp(q,c,x)
def pct_below(x,w,v): return w[x<=v].sum()/w.sum()*100
out=[]
tot_ocup=d.w.sum()
groups={"ocupados_con_ingreso>0": d[d.INGLABO>0],
        "asalariados_privados_y_gobierno_con_ingreso>0": d[(d.INGLABO>0)&(d.P6430.isin([1,2]))]}
rows=[]
for g,s in groups.items():
    x=s.INGLABO.values.astype(float); w=s.w.values
    mean=np.average(x,weights=w); med=wq(x,w,0.5)
    r=dict(grupo=g,n_muestra=len(s),poblacion_expandida=w.sum(),media=mean,mediana=med,
           p90=wq(x,w,0.9),p95=wq(x,w,0.95),p99=wq(x,w,0.99),
           pct_sobre_media=100-pct_below(x,w,mean),
           n_mas_10M=w[x>10_000_000].sum(),pct_mas_10M=w[x>10_000_000].sum()/w.sum()*100,
           n_muestra_mas_10M=int((x>10_000_000).sum()))
    for v in [2e6,4e6,10e6,15e6]:
        r[f"percentil_{int(v/1e6)}M"]=pct_below(x,w,v)
    rows.append(r)
r=pd.DataFrame(rows)
r["total_ocupados_expandido(incl. sin ingreso)"]=tot_ocup
r["n_ocupados_sin_ingreso_o_missing"]=int((~(d.INGLABO>0)).sum())
pd.set_option("display.width",250); print(r.T)
r.to_csv("distribucion_geih_2026.csv",index=False)

# Percentil con heaping: % estrictamente por debajo y % hasta (inclusive)
rows2=[]
for g,s in groups.items():
    x=s.INGLABO.values.astype(float); w=s.w.values; W=w.sum()
    for v in [2e6,3.5e6,4e6,9e6,10e6,15e6]:
        rows2.append(dict(grupo=g,umbral=int(v),pct_estrict_debajo=w[x<v].sum()/W*100,pct_hasta_incl=w[x<=v].sum()/W*100,
                          pct_estrict_encima=w[x>v].sum()/W*100,personas_estrict_encima=w[x>v].sum()))
r2=pd.DataFrame(rows2); print(r2.to_string()); r2.to_csv("percentiles_geih_2026.csv",index=False)
