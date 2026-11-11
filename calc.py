"""
Impacto de la 'Ley de Rescate Económico' (PL 477/2026 Cámara - 328/2026 Senado, texto radicado 29-oct-2026,
Gaceta del Congreso 1717 del 4-nov-2026) sobre asalariados residentes con 2, 4, 10 y 15 M COP/mes.
Ejercicio ESTÁTICO con parámetros 2026 (UVT y SMMLV 2026) para norma vigente y reforma.
Ejecutar: python3 calc.py  -> resultados.csv, canasta_iva.csv, canasta_resumen.csv
"""
import pandas as pd, numpy as np

UVT = 52_374            # Res. DIAN 000238 de 15-dic-2025
SMMLV = 1_750_905       # Decreto 0159 de 19-feb-2026 (transitorio)
NIVELES = [2_000_000, 4_000_000, 10_000_000, 15_000_000]
MESES = 12              # SUPUESTO: ingreso anual = 12 x mensual (sin prima/cesantías ni auxilio de transporte)

# ---------------- Tablas art. 241 ET ----------------
TABLA_VIG = [(0,1090,0.00,0),(1090,1700,0.19,0),(1700,4100,0.28,116),(4100,8670,0.33,788),
             (8670,18970,0.35,2296),(18970,31000,0.37,5901),(31000,1e12,0.39,10352)]
TABLA_REF = [(0,720,0.00,0),(720,1090,0.09,0),(1090,1700,0.19,33),(1700,4100,0.28,149),
             (4100,8670,0.33,821),(8670,1e12,0.39,2329)]          # art. 48 PL 477/2026

def impuesto_uvt(base_uvt, tabla):
    for lo,hi,t,fijo in tabla:
        if base_uvt <= hi:
            return 0.0 if t==0 else (base_uvt-lo)*t + fijo
    raise ValueError

def salud_trab(m, reforma):
    if not reforma: return 0.04
    s = m/SMMLV                                                  # art. 21 PL (art. 204 Ley 100)
    for lim,t in [(2,0.04),(4,0.055),(5,0.06),(10,0.065),(15,0.07),(20,0.075),(25,0.08)]:
        if s <= lim: return t
    return 0.08

def fsp(m):  # Fondo de Solidaridad Pensional vigente 2026 (Ley 797/2003 art. 27; Ley 2381/2024 aún no rige)
    s = m/SMMLV
    if s < 4: return 0.0
    if s < 16: return 0.01
    if s < 17: return 0.012
    if s < 18: return 0.014
    if s < 19: return 0.016
    if s < 20: return 0.018
    return 0.02

def renta(m, reforma):
    S = m*MESES
    ibc = min(m, 25*SMMLV)
    tasa_salud = salud_trab(m, reforma)
    incr = ibc*MESES*(tasa_salud + 0.04 + fsp(m))               # INCRNGO arts. 55-56 ET
    neto = S - incr
    tope25 = (630 if reforma else 790)*UVT                       # art. 206-10 (art. 47 PL)
    tope_glob = (1180 if reforma else 1340)*UVT                  # art. 336 (art. 49 PL)
    exenta = min(0.25*neto, tope25)
    benef = min(exenta, 0.40*neto, tope_glob)
    base = neto - benef
    imp = impuesto_uvt(base/UVT, TABLA_REF if reforma else TABLA_VIG)*UVT
    return dict(salud_trab_pct=tasa_salud, aporte_salud_anual=ibc*MESES*tasa_salud,
                incrngo=incr, ingreso_neto=neto, renta_exenta_aplicada=benef,
                base_gravable=base, base_uvt=base/UVT, impuesto_renta_anual=imp)

# ---------------- Canasta de mercado (IVA) ----------------
# Pesos por subclase IPC base 2018 (derivados de ENPH 2016-17) -> ipc2018_subclases_alimentos.csv
# IVA vigente (arts. 424, 468-1, 477 ET) y con reforma desde 1-ene-2028 (arts. 42, 45, 46 y 106 PL).
# share_cambia = fracción de la subclase que cambia de tarifa (ESTIMADO cuando la subclase es mixta).
MAPA = {  # cod: (iva_vig_parte_que_cambia, iva_ref_parte_que_cambia, share_cambia, iva_resto(sin cambio), nota)
 "01110100":(0,0,0,0,"Arroz: exento, sigue exento"),
 "01110200":(0.05,0.19,1,0,"Pastas 5%->19% (468-1 eliminado)"),
 "01110300":(0.05,0.19,1,0,"Avena hojuelas 5%->19%"),
 "01110500":(0.05,0.19,1,0,"Harina de trigo 5%->19%"),
 "01110600":(0.05,0.19,1,0,"Harinas de maíz 5%->19% (11.02); maíz trillado excl.->19% (ESTIMADO todo a 5%)"),
 "01110800":(0,0,0,0,"Pan y arepa: excluido, sigue excluido (19.05)"),
 "01119800":(0,0,0,0.19,"Harina tortas/cereal 19% sin cambio; arepa precocida sigue excluida (ESTIMADO sin cambio)"),
 "01119900":(0,0,0,0.19,"Galletas 19% sin cambio"),
 "01120100":(0,0,0,0,"Res: exento sigue exento"),
 "01120200":(0,0,0,0,"Cerdo: exento sigue exento"),
 "01120300":(0,0,0,0,"Pollo: exento sigue exento"),
 "01120500":(0.05,0.0,0.4,0.19,"Mortadela/salchichón 5%->exento (40% ESTIMADO); salchicha/jamón/chorizo 19%"),
 "01130300":(0,0,0,0,"Pescado fresco exento; enlatado sin cambio (ESTIMADO sin cambio)"),
 "01140100":(0,0,0,0,"Leche exenta sigue exenta"),
 "01140200":(0.0,0.19,0.7,0.19,"Queso fresco exento->19% (no está en nuevo art. 477); 70% queso fresco ESTIMADO"),
 "01140500":(0,0,0,0,"Huevos exentos siguen exentos"),
 "01149900":(0,0,0,0.19,"Yogur/kumis 19% sin cambio (ESTIMADO)"),
 "01150100":(0,0,0,0.19,"Aceite refinado 19% sin cambio (solo aceites en bruto en 468-1)"),
 "01150200":(0,0,0,0.19,"Mantequilla 19%"),
 "01150500":(0,0,0,0.19,"Margarinas 19%"),
 "01160200":(0,0,0,0.19,"Pulpa/congeladas 19% (ESTIMADO)"),
 "01160300":(0,0,0,0.19,"Frutos secos 19% (ESTIMADO)"),
 "01160500":(0,0.19,1,0,"Naranjas excluidas->19% (08.05 sale del 424)"),
 "01160600":(0,0.19,1,0,"Bananos excluidos->19% (08.03)"),
 "01160700":(0,0.19,1,0,"Tomate de árbol excluido->19% (08.10)"),
 "01160800":(0,0.19,1,0,"Moras excluidas->19% (08.10)"),
 "01160900":(0,0.19,1,0,"Frutas frescas excluidas->19% (cap. 08)"),
 "01170200":(0,0.19,1,0,"Legumbres secas (fríjol, lenteja 07.13) excluidas->19%"),
 "01170300":(0,0,0,0.19,"Conservas 19% sin cambio"),
 "01170400":(0,0.19,1,0,"Plátano excluido->19% (08.03)"),
 "01170500":(0,0,0,0,"Papa excluida sigue excluida (07.01)"),
 "01170600":(0,0,0,0,"Yuca excluida sigue excluida (07.14)"),
 "01171100":(0,0,0,0.19,"Derivados tubérculos 19% (ESTIMADO)"),
 "01171200":(0,0,0,0,"Arracacha/ñame siguen excluidos (07.14)"),
 "01171300":(0,0.19,1,0,"Tomate excluido->19% (07.02)"),
 "01171400":(0,0.19,1,0,"Cebolla excluida->19% (07.03)"),
 "01171500":(0,0.19,1,0,"Zanahoria excluida->19% (07.06)"),
 "01171600":(0,0.19,0.75,0,"Hortalizas frescas excl.->19%; hortalizas de vaina (07.08) siguen excl. (25% ESTIMADO)"),
 "01180100":(0.05,0.19,1,0,"Azúcar 5%->19%"),
 "01180200":(0,0,0,0,"Panela sigue excluida"),
 "01180300":(0,0.19,0.5,0.19,"Miel/bocadillo artesanal excl.->19%; mermelada 19% (50% ESTIMADO)"),
 "01180500":(0,0,0,0.19,"Dulces 19%"),
 "01180600":(0,0,0,0.19,"Helados 19%"),
 "01180700":(0,0,0,0.19,"Gelatinas 19%"),
 "01190100":(0,0,0,0.19,"Salsas 19%"),
 "01190200":(0,0.19,1,0,"Sal excluida->19% (25.01 sale del 424)"),
 "01190500":(0,0,0,0.19,"Caldos 19%"),
 "01190600":(0,0,0,0.19,"Frituras 19%"),
 "01190800":(0,0.19,0.5,0.19,"Condimentos: hierbas frescas excl.->19% (50% ESTIMADO)"),
 "01191100":(0,0,0,0,"Fórmulas lácteas exentas siguen exentas"),
 "01199900":(0,0,0,0.19,"Precocidos 19%"),
 "01210100":(0.05,0.19,1,0,"Café 5%->19%"),
 "01210200":(0.05,0.19,0.7,0.19,"Chocolate de mesa 5%->19% (70% ESTIMADO); instantáneo 19%"),
 "01210300":(0,0,0,0.19,"Té 19%"),
 "01220100":(0,0,0,0,"Agua sin azúcar sigue excluida (22.01)"),
 "01220600":(0,0,0,0.19,"Jugos empacados 19%"),
 "01220700":(0,0,0,0.19,"Refrescos en polvo 19%"),
 "01221100":(0,0,0,0.19,"Gaseosas 19%"),
 "01221200":(0,0,0,0.19,"Energizantes 19%"),
}

def canasta(col):
    w = pd.read_csv("ipc2018_subclases_alimentos.csv", dtype={"cod":str})
    w["peso"] = w[col].astype(float)/w[col].astype(float).sum()
    rows=[]
    for _,r in w.iterrows():
        tv,tr,sh,tres,nota = MAPA[r.cod]
        # factor de precio con traslado total: (1+t_ref)/(1+t_vig) en la parte que cambia
        dp = sh*((1+tr)/(1+tv)-1)
        rows.append(dict(cod=r.cod, subclase=r.nombre, peso=r.peso, iva_vig=tv if sh>0 else tres,
                         iva_ref=tr if sh>0 else tres, share_cambia=sh, var_precio=dp, nota=nota))
    return pd.DataFrame(rows)

def sobrecosto_mensual(mercado, col, traslado=1.0):
    c = canasta(col)
    return mercado*(c.peso*c.var_precio).sum()*traslado

# Variante B (mercado crece con el ingreso). ESTIMADO:
# gasto total mensual por decil ENPH 2016-17 (boletín DANE, miles COP) x peso de alimentos de la clase IPC.
GASTO_DECIL_2017 = {5:1331, 8:2151, 10:5867}
PESO_ALIM = {"vulnerables":0.2224, "media":0.1580, "altos":0.0816}   # IPC base 2018 (ENPH)
MAP_NIVEL = {2_000_000:(5,"vulnerables"), 4_000_000:(8,"media"), 10_000_000:(10,"altos"), 15_000_000:(10,"altos")}
def mercado_variante_b(m):
    d,cl = MAP_NIVEL[m]
    base = GASTO_DECIL_2017[5]*PESO_ALIM["vulnerables"]
    f = GASTO_DECIL_2017[d]*PESO_ALIM[cl]/base
    if m==15_000_000: f *= (15/10)**0.3   # SUPUESTO: elasticidad-ingreso del gasto en alimentos 0,3 dentro del decil 10
    return 500_000*f, cl

if __name__=="__main__":
    out=[]
    for m in NIVELES:
        v=renta(m,False); r=renta(m,True)
        mB, clB = mercado_variante_b(m)
        rec=dict(ingreso_mensual=m, ingreso_smmlv=round(m/SMMLV,2),
                 renta_vig_anual=v["impuesto_renta_anual"], renta_ref_anual=r["impuesto_renta_anual"],
                 base_uvt_vig=v["base_uvt"], base_uvt_ref=r["base_uvt"],
                 salud_vig_pct=v["salud_trab_pct"], salud_ref_pct=r["salud_trab_pct"],
                 aporte_salud_vig_anual=v["aporte_salud_anual"], aporte_salud_ref_anual=r["aporte_salud_anual"])
        rec["delta_renta_mes"]=(rec["renta_ref_anual"]-rec["renta_vig_anual"])/12
        rec["delta_salud_mes"]=(rec["aporte_salud_ref_anual"]-rec["aporte_salud_vig_anual"])/12
        rec["tet_renta_vig_%"]=rec["renta_vig_anual"]/(m*12)*100
        rec["tet_renta_ref_%"]=rec["renta_ref_anual"]/(m*12)*100
        # IVA mercado
        rec["ivaA_500k_tras100_mes"]=sobrecosto_mensual(500_000,"total",1.0)
        rec["ivaA_500k_tras50_mes"]=sobrecosto_mensual(500_000,"total",0.5)
        rec["mercadoB_mes"]=mB; rec["mercadoB_clase_ipc"]=clB
        rec["ivaB_tras100_mes"]=sobrecosto_mensual(mB,clB,1.0)
        rec["ivaB_tras50_mes"]=sobrecosto_mensual(mB,clB,0.5)
        for k in ["delta_renta_mes","delta_salud_mes","ivaA_500k_tras100_mes","ivaB_tras100_mes"]:
            rec[k.replace("_mes","_%ing")]=rec[k]/m*100
        # Sensibilidad EfectIVA (solo plausible en 2M si el hogar está clasificado como vulnerable en Sisbén): devolución 30% y 50%
        if m==2_000_000:
            rec["ivaA_2M_con_EfectIVA30_mes"]=rec["ivaA_500k_tras100_mes"]*0.7
            rec["ivaA_2M_con_EfectIVA50_mes"]=rec["ivaA_500k_tras100_mes"]*0.5
        rec["total_renta+ivaA_mes"]=rec["delta_renta_mes"]+rec["ivaA_500k_tras100_mes"]
        rec["total_renta+ivaB_mes"]=rec["delta_renta_mes"]+rec["ivaB_tras100_mes"]
        rec["total_renta+salud+ivaB_mes"]=rec["total_renta+ivaB_mes"]+rec["delta_salud_mes"]
        for k in ["total_renta+ivaA_mes","total_renta+ivaB_mes","total_renta+salud+ivaB_mes"]:
            rec[k.replace("_mes","_%ing")]=rec[k]/m*100
        out.append(rec)
    res=pd.DataFrame(out); res.to_csv("resultados.csv",index=False)
    pd.set_option("display.width",250); pd.set_option("display.float_format",lambda x:f"{x:,.2f}")
    print(res.T.to_string())
    cs=[]
    for col in ["total","pobres","vulnerables","media","altos"]:
        c=canasta(col); c.insert(0,"canasta_ipc",col); cs.append(c)
    allc=pd.concat(cs); allc.to_csv("canasta_iva.csv",index=False)
    allc=allc.reset_index(drop=True)
    resumen=allc.assign(contrib=allc.peso*allc.var_precio, pc=allc.peso*allc.share_cambia).groupby("canasta_ipc").agg(
        alza_precio_canasta_pct=("contrib",lambda s:s.sum()*100),
        peso_que_cambia_pct=("pc",lambda s:s.sum()*100))
    resumen.to_csv("canasta_resumen.csv"); print(resumen)
