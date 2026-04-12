import pandas as pd
import numpy as np
import math

# 1. CARGAR Y LIMPIAR DATOS
nombre_archivo = 'datos_filtrados.xlsx' 
df = pd.read_excel(nombre_archivo)

# Limpieza estricta: extraer solo los valores númericos
df['Edad'] = df['Edad'].astype(str).str.extract(r'(\d+)').astype(float)
df['Población'] = df['Población'].astype(str).str.replace(' ', '', regex=False)
df['Población'] = pd.to_numeric(df['Población'], errors='coerce')
df = df.dropna(subset=['Edad', 'Población'])

# 2. AGRUPACIÓN DE DATOS (Las 5 etapas)
bins = [-1, 12, 18, 25, 60, 150]
etapas = ['Niñez (0-12)', 'Adolescencia (13-18)', 'Juventud (19-25)', 'Adultez (26-60)', 'Vejez (61+)']

df['Etapa'] = pd.cut(df['Edad'], bins=bins, labels=etapas)
tabla = df.groupby('Etapa', observed=True)['Población'].sum().reset_index()
tabla.columns = ['Etapa', 'fi'] # fi = Frecuencia Absoluta

# Marcas de clase (xi)
tabla['xi'] = [6, 15.5, 22, 43, 80.5]   

# 3. CÁLCULO DE MEDIDAS DE DISPERSIÓN
N = tabla['fi'].sum()

# a) Calculamos la Media Exacta primero (es necesaria para la dispersión)
tabla['fi_xi'] = tabla['fi'] * tabla['xi']
media_exacta = tabla['fi_xi'].sum() / N

# b) VARIANZA: Sumatoria de [ fi * (xi - media)^2 ] / N
# Al ser datos de todo el país (INEGI), usamos fórmula poblacional (dividir entre N, no N-1)
tabla['xi_menos_media_cuadrado'] = (tabla['xi'] - media_exacta) ** 2
tabla['fi_dispersion'] = tabla['fi'] * tabla['xi_menos_media_cuadrado']

varianza_exacta = tabla['fi_dispersion'].sum() / N

# c) DESVIACIÓN ESTÁNDAR: Raíz cuadrada de la varianza
desviacion_exacta = math.sqrt(varianza_exacta)

# 4. REDONDEO Y RESULTADOS (Regla del proyecto)
def redondear_especial(valor):
    if valor < 20: return round(valor) 
    else: return math.ceil(valor / 10.0) * 10

print("="*50)
print(" MEDIDAS DE DISPERSIÓN (DATOS AGRUPADOS)")
print("="*50)
print(f"Población Total (N): {N:,.0f}\n")

print("Varianza (\u03C3\u00B2 o s\u00B2):")
print(f"  Exacta:   {varianza_exacta:.2f}")
print(f"  Ajustada: {redondear_especial(varianza_exacta)}\n")

print("Desviación Estándar (\u03C3 o s):")
print(f"  Exacta:   {desviacion_exacta:.2f} años")
print(f"  Ajustada: {redondear_especial(desviacion_exacta)} años")
print("="*50)