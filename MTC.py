import pandas as pd
import numpy as np
import math

# 1. CARGAR Y LIMPIAR DATOS
nombre_archivo = 'datos_filtrados.xlsx' 
df = pd.read_excel(nombre_archivo)

# Limpieza estricta: extraer números y quitar espacios
df['Edad'] = df['Edad'].astype(str).str.extract(r'(\d+)').astype(float)
df['Población'] = df['Población'].astype(str).str.replace(' ', '', regex=False)
df['Población'] = pd.to_numeric(df['Población'], errors='coerce')
df = df.dropna(subset=['Edad', 'Población'])

# 2. AGRUPACIÓN DE DATOS (Las 5 etapas de tu proyecto)
# Definimos los límites de los grupos: Niñez, Adolescencia, Juventud, Adultez, Vejez
bins = [-1, 12, 18, 25, 60, 150]
etapas = ['Niñez (0-12)', 'Adolescencia (13-18)', 'Juventud (19-25)', 'Adultez (26-60)', 'Vejez (61+)']

# Clasificamos a cada año en su respectiva etapa y sumamos la población
df['Etapa'] = pd.cut(df['Edad'], bins=bins, labels=etapas)
tabla = df.groupby('Etapa', observed=True)['Población'].sum().reset_index()
tabla.columns = ['Etapa', 'fi'] # fi = Frecuencia Absoluta

# Definimos variables matemáticas para las fórmulas de datos agrupados
tabla['Li'] = [0, 13, 19, 26, 61]       # Límite Inferior de cada clase
tabla['A'] = [13, 6, 7, 35, 40]         # Amplitud de cada clase
tabla['xi'] = [6, 15.5, 22, 43, 80.5]   # Marcas de clase (Punto medio)
tabla['Fi'] = tabla['fi'].cumsum()      # Frecuencia Acumulada

# 3. CÁLCULO DE MEDIDAS (Fórmulas para Datos Agrupados)
N = tabla['fi'].sum()

# MEDIA: Sumatoria de (fi * xi) / N
tabla['fi_xi'] = tabla['fi'] * tabla['xi']
media_exacta = tabla['fi_xi'].sum() / N

# MEDIANA: Li + ((N/2 - F_anterior) / fi) * A
mitad_N = N / 2
idx_me = tabla[tabla['Fi'] >= mitad_N].index[0] # Encuentra la clase de la mediana
Li_me = tabla.loc[idx_me, 'Li']
fi_me = tabla.loc[idx_me, 'fi']
F_ant_me = tabla.loc[idx_me - 1, 'Fi'] if idx_me > 0 else 0
A_me = tabla.loc[idx_me, 'A']
mediana_exacta = Li_me + ((mitad_N - F_ant_me) / fi_me) * A_me

# MODA: Li + (d1 / (d1 + d2)) * A
idx_mo = tabla['fi'].idxmax() # Encuentra la clase modal
Li_mo = tabla.loc[idx_mo, 'Li']
Li_mo = tabla.loc[idx_mo, 'Li']
fi_mo = tabla.loc[idx_mo, 'fi']
fi_ant = tabla.loc[idx_mo - 1, 'fi'] if idx_mo > 0 else 0
fi_sig = tabla.loc[idx_mo + 1, 'fi'] if idx_mo < len(tabla) - 1 else 0
A_mo = tabla.loc[idx_mo, 'A']

d1 = fi_mo - fi_ant
d2 = fi_mo - fi_sig
moda_exacta = Li_mo + (d1 / (d1 + d2)) * A_mo

# 4. REDONDEO Y RESULTADOS
def redondear_especial(valor):
    if valor < 20: return round(valor) 
    else: return math.ceil(valor / 10.0) * 10

print("="*50)
print(" MEDIDAS DE TENDENCIA CENTRAL (DATOS AGRUPADOS)")
print("="*50)
print(f"Población Total (N): {N:,.0f}\n")
print(f"Media (\u0078\u0304):  Exacta: {media_exacta:.2f}  | Ajustada: {redondear_especial(media_exacta)}")
print(f"Mediana (Me): Exacta: {mediana_exacta:.2f}  | Ajustada: {redondear_especial(mediana_exacta)}")
print(f"Moda (Mo):    Exacta: {moda_exacta:.2f}  | Ajustada: {redondear_especial(moda_exacta)}")
print("="*50)