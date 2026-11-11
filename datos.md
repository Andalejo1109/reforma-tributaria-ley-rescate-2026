# Ley de Rescate Económico: impacto en asalariados de 2, 4, 10 y 15 M COP/mes
Fecha del análisis: 11-nov-2026 (America/Bogota). Ejercicio estático con parámetros 2026. Solo educativo.

## 0. Estado del proyecto (VERIFICADO)
- Se llama **Proyecto de Ley 477 de 2026 Cámara / 328 de 2026 Senado**, "Ley de Rescate Económico". La prensa le dice "Ley de Rescate Fiscal". Lo radicó el MinHacienda (ministro Miguel Gómez) el **29-oct-2026**. Tiene 106 artículos.
  - Texto radicado: https://www.camara.gov.co/wp-content/uploads/2026/10/proyectos-ley/documentos/proyecto-36548/PROYECTO-DE-LEY-Rescate-Economico-2026-VSD-RADICADA-1.pdf
  - Gaceta del Congreso 1717, 4-nov-2026 (copia): https://www.sindesena.org/wp-content/uploads/2026/11/03.1GACETA-PL-477-CAMARA-1.pdf
  - Resumen de Deloitte del 30-oct-2026: https://www.deloitte.com/content/dam/assets-zone4/latam/es/docs/services/tax/2026/Flash-Extraordinario-Ley-de-Rescate-Economico.pdf
- **Etapa:** todavía no ha tenido el primer debate y no hay ponencia radicada. El 10-nov-2026 se designaron ponentes en el Senado: David Barguil (Comisión 3ª) y Carlos Mario Farelo (Comisión 4ª). Los ponentes de la Cámara siguen pendientes. Hay disputa sobre si el trámite va por comisiones económicas conjuntas o solo por las terceras. Las sesiones ordinarias terminan el 16-dic-2026.
  - El Nuevo Siglo, 10-nov-2026: https://www.elnuevosiglo.com.co/politica/senado-designa-ponentes-de-la-ley-de-rescate-fiscal-del-gobierno
  - El Colombiano, 10-nov-2026: https://www.elcolombiano.com/negocios/senado-designa-ponentes-para-debatir-ley-de-rescate-fiscal-EH43443520
  - Portafolio, 9-nov-2026: https://www.portafolio.co/economia/el-tiempo-pasa-y-se-nos-van-las-ordinarias-quedan-menos-de-6-semanas-para-poder-aprobar-la-reforma-tributaria-506008
- Versión usada en el cálculo: **el texto radicado**, porque es el único que existe.

## 1. Parámetros (VERIFICADO)
- UVT 2026 = $52.374, fijada por la Res. DIAN 000238 del 15-dic-2025: https://normograma.dian.gov.co/dian/compilacion/docs/resolucion%5Fdian%5F0238%5F2025.htm
- SMMLV 2026 = $1.750.905, fijado por el Decreto 0159 del 19-feb-2026 (transitorio): https://dapre.presidencia.gov.co/normativa/normativa/DECRETO%20No.%200159%20DEL%2019%20DE%20FEBRERO%20DE%202026.pdf
- Estatuto Tributario vigente (arts. 241, 206-10, 336, 424, 468-1, 477) en el normograma DIAN: https://normograma.dian.gov.co/dian/compilacion/docs/estatuto_tributario.htm
- Cambios del PL que se usan (Gaceta 1717):
  - art. 47: tope de la renta exenta del 25 % pasa de 790 a 630 UVT.
  - art. 48: nueva tabla del art. 241. Va de 0 a 720 UVT al 0 %, de 720 a 1.090 al 9 %, luego 19 %, 28 % y 33 %, y 39 % desde 8.670 UVT.
  - art. 49: el límite global de exentas y deducciones pasa de 1.340 a 1.180 UVT.
  - art. 106: deroga la deducción de 72 UVT por dependiente.
  - art. 21: la cotización de salud del trabajador pasa a ser progresiva: 4 % hasta 2 SMLMV, 5,5 % de 2 a 4, 6 % de 4 a 5, 6,5 % de 5 a 10, 7 % de 10 a 15, 7,5 % de 15 a 20 y 8 % de 20 a 25.
  - arts. 42, 45, 46 y 106: nuevas listas de IVA para excluidos (424) y exentos (477), y se elimina la tarifa del 5 % (468-1). Rigen **desde el 1-ene-2028**. La renta y la salud rigen desde 2027.
- FSP 2026: 1 % desde 4 SMMLV y escalonado desde 16 SMMLV, según la Ley 797 de 2003. La Ley 2381 de 2024 rige desde abr-2027 (Sentencia C-264 de 2026). **Esto proviene de fuentes secundarias** (https://e7.legal/reforma-pensional-que-decidio-la-corte-en-la-sentencia-c-264-de-2026/). En los cuatro niveles el FSP es igual en ambos escenarios, así que no cambia el delta.

## 2. Supuestos (SUPUESTO)
- Asalariado residente con salario ordinario. Se asume ingreso anual = 12 × el mensual, sin prima, cesantías ni auxilio de transporte.
- Solo renta de trabajo. Sin dependientes, sin intereses de vivienda y sin aportes voluntarios.
- Las deducciones son las cotizaciones obligatorias del trabajador (salud, 4 % de pensión y FSP), tratadas como INCRNGO. El IBC es igual al salario.
- Se usan los parámetros 2026 en los dos escenarios para aislar el efecto de las reglas. En la realidad, la renta reformada aplicaría desde el año gravable 2027 y el IVA desde 2028, con UVT indexada.
- La cotización de salud no es un impuesto, pero reduce el ingreso disponible. Por eso se muestra en una línea aparte.

## 3. Canasta de mercado e IVA (composición ESTIMADA)
- Composición de la canasta: pesos por subclase del IPC base 2018, que salen de la ENPH 2016-17, por nivel de ingreso (pobres, vulnerables, clase media, altos). Fuente: DANE, "Estructura histórica de ponderaciones y canasta IPC 2026", hoja 2018: https://www.dane.gov.co/files/operaciones/IPC/Estructura-historica-ponderaciones-y-canasta-IPC-2026.xls . Se guardaron en ipc2018_subclases_alimentos.csv.
- Tarifa de cada subclase antes y después de la reforma: canasta_iva.csv. Cuando una subclase mezcla productos, la fracción que cambia de tarifa es ESTIMADA y queda anotada en calc.py.
- **Productos que cambian según el articulado (VERIFICADO en el texto):**
  - Pasan de excluido a 19 %: frutas frescas (todo el capítulo 08), plátano, tomate, cebolla, zanahoria y demás hortalizas frescas (salvo las hortalizas de vaina, 07.08), legumbres secas como fríjol y lenteja (07.13), maíz para consumo y maíz trillado, sal, miel, café en grano sin tostar y los productos artesanales a base de leche o guayaba.
  - Pasa de exento a 19 %: el queso fresco (04.06.10), que ya no aparece en el nuevo art. 477.
  - Pasan del 5 % al 19 %: café, azúcar, chocolate de mesa, pastas, harinas de trigo y de maíz, y avena.
  - Pasan del 5 % a exento: salchichón, butifarra y mortadela.
  - No cambian: arroz, carnes (res, cerdo, pollo), pescado, leche, huevos y fórmulas infantiles, que siguen exentos; y papa, yuca, pan y arepa, panela, agua, energía y gas, que siguen excluidos.
  - ⚠️ La exposición de motivos dice que los "granos" siguen excluidos, pero la lista del art. 42 no incluye la partida 07.13 (legumbres secas). Esta contradicción hay que confirmarla en la ponencia.
- Supuesto de traslado: 100 % del IVA al precio, con sensibilidad al 50 %. No se modela el IVA de insumos ya incorporado en los bienes excluidos.
- **Variante A:** mercado fijo de $500.000 al mes, igual para los cuatro niveles, con la canasta "total".
- **Variante B (ESTIMADO):** el valor del mercado crece con el ingreso. Se calcula como el gasto total por decil de la ENPH (D5 $1.331k, D8 $2.151k, D10 $5.867k, en pesos de 2017; boletín https://www.dane.gov.co/files/investigaciones/boletines/enph/boletin-enph-2017.pdf) por el peso de alimentos de la clase IPC (vulnerables 22,24 %, media 15,80 %, altos 8,16 %). Se ancla en $500k para el nivel de 2M y se usa la canasta de cada clase.
  - Asignación de niveles: 2M → D5/vulnerables, 4M → D8/media, 10M y 15M → D10/altos.
  - Para 15M se agrega una elasticidad de 0,3 dentro del decil 10, que es un SUPUESTO.
- EfectIVA: la devolución es del 100 % en los deciles 1 a 3 y del 50 %, 40 % y 30 % en los deciles 4 a 6, con tope de 5,5 UVT por persona al mes. Para estos cuatro niveles probablemente no aplica. Solo el de 2M podría recibir una devolución parcial si su hogar está clasificado como vulnerable en el Sisbén, y por eso se muestra una sensibilidad del 30 % y del 50 %.

## 4. Distribución del ingreso
- Ingreso laboral mensual (INGLABO) de la GEIH DANE de ene a ago-2026 (microdatos del catálogo 900: https://microdatos.dane.gov.co/index.php/catalog/900/get-microdata). Se juntan los 8 meses con FEX_C18/8. Script: geih_dist.py. Salidas: distribucion_geih_2026.csv y percentiles_geih_2026.csv. **Cálculo propio sobre microdatos oficiales.** Los percentiles en valores redondos tienen acumulación de respuestas, por eso se reportan los rangos "<" y "≤".
- Ingreso per cápita de la unidad de gasto, 2025: $1.281.590 al mes (DANE, Pobreza Monetaria 2025: https://www.dane.gov.co/files/operaciones/PM/pres-PM-2025.pdf).
- DIAN, año gravable 2024: 6.521.502 declaraciones de personas naturales, con $5,7 billones de impuesto a cargo al presentar la declaración y un recaudo total de $23,6 billones (Comunicado 096 del 28-oct-2025: https://www.dian.gov.co/Prensa/Paginas/NG-Comunicado-de-Prensa-096-2025.aspx).
- Referencias de MinHacienda en la exposición de motivos (Gaceta 1717): con la norma actual se empieza a pagar renta desde unos $9M al mes, lo que según ellos equivale al "4 % de asalariados con mayores ingresos". Con la reforma se pagaría desde unos $5,5M ($5M con todas las medidas). Además, el 75,2 % de los asalariados gana 2 SMLMV o menos.

## 5. Resultados principales (de resultados.csv)
| Ingreso/mes | Percentil (ocupados) | Renta vigente/año | Renta reforma/año | Δ renta/mes | Δ salud/mes | IVA mercado A/mes | IVA mercado B/mes | Total renta+IVA B (% ingreso) | Total + salud (% ingreso) |
|---|---|---|---|---|---|---|---|---|---|
| 2M | p60–p70 | 0 | 0 | 0 | 0 | 19.814 (0,99 %) | 19.072 (0,95 %) | 0,95 % | 0,95 % |
| 4M | p88–p90 | 0 | 0 | 0 | 60.000 | 19.814 (0,50 %) | 22.418 (0,56 %) | 0,56 % | 2,06 % |
| 10M | p98 | 4.714.345 | 6.015.187 | 108.404 | 250.000 | 19.814 (0,20 %) | 37.632 (0,38 %) | 1,46 % | 3,96 % |
| 15M | p99,1–99,2 | 15.543.360 | 18.238.928 | 224.631 | 375.000 | 19.814 (0,13 %) | 42.500 (0,28 %) | 1,78 % | 4,28 % |
Tasa efectiva de renta: 10M pasa de 3,93 % a 5,01 % y 15M de 8,64 % a 10,13 %. Con traslado del 50 % los montos de IVA se reducen a la mitad. Alza de precio de la canasta de alimentos: 3,96 % en la canasta total (3,81 % para pobres y vulnerables, 3,91 % media, 4,65 % altos).
