# -*- coding: utf-8 -*-
""" Descripción
Análisis de frecuencia
Archivos compilados de datos observacionales CR2 

Sitio web: http://www.cr2.cl/datos-de-precipitacion/
Archivo: cr2_prDaily_2018_ghcn.zip

José Ignacio Saldías 
jose.saldias@cigiden.cl
"""

# Incluidas en python
import os

# Instaladas a través de Anaconda
import pandas as pd
import numpy as np
import scipy.stats as ss

# =============================================================================
# Se recomienda la lectura previa del archivo "examinacion_estaciones.py"
# =============================================================================

directorio = r'C:\Users\saldi\OneDrive\Escritorio\Rutinas Github'
n_archivo = 'cr2_prDaily_2018_ghcn.txt'     # Nombre del archivo
r_archivo = os.path.join(directorio, n_archivo) # Ruta absoluta al archivo
# Lectura de archivo selección quinta normal 
df = pd.read_csv(
    r_archivo,
    index_col = 0,
    skiprows = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    na_values = (-9999)
    )['Quinta Normal Santiago']
# Resampleo
df.index = pd.to_datetime(df.index.values)
df = df.resample('YS').max().dropna()
# Numero de clases
n_clases = np.floor(5 * np.log10(len(df))).astype(int)
# Curva Empírica
y, x = np.histogram(df.values, bins = n_clases)
# Ajuste Funcion de probabilidad Gumbel
args = ss.gumbel_r.fit(df.values)
esperado = []
for i in range(len(x)-1):
    li = ss.gumbel_r.cdf(x[i], *args)
    ls = ss.gumbel_r.cdf(x[i+1], *args)
    esperado.append((ls - li)*len(df))
esperado = np.array(esperado)  
# Test Chi Cuadrado H0 ~ Datos siguen distribución
alpha = 0.05
grados_de_libertad = len(args)
chi_muestral = ss.chisquare(y, esperado, grados_de_libertad)
chi_estadistico = ss.chi2.ppf(1 - alpha / 2, grados_de_libertad)
# Resultados: si chi_estadistico > chi_muestral se rechaza H0