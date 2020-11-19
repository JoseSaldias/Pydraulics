# -*- coding: utf-8 -*-
""" Descripción
Lectura de datos de precipitación.
Archivos compilados de datos observacionales CR2 

Sitio web: http://www.cr2.cl/datos-de-precipitacion/
Archivo: cr2_prDaily_2018_ghcn.zip

José Ignacio Saldías 
jose.saldias@cigiden.cl
"""

# =============================================================================
# Dependencias requeridas
# =============================================================================

# Incluidas en python
import os
import time

# Instaladas a través de Anaconda
import numpy as np
import pandas as pd

# =============================================================================
# Manejo de Directorio
# =============================================================================

# Nombres
dir_loc = os.getcwd()                       # Directorio local
n_archivo = 'cr2_prDaily_2018_ghcn.txt'     # Nombre del archivo

# Rutas
r_archivo = os.path.join(dir_loc, n_archivo) # Ruta absoluta al archivo


# =============================================================================
# Guía general para la extracción de datos y cómputos iniciales
# =============================================================================

# Lectura de datos
print('\nLeyendo archivo: {}'.format(n_archivo))    # Punto de seguimiento
inicio = time.process_time()             # Medición de desempeño
df = pd.read_csv(r_archivo,             # Ruta del archivo a abrir
                 na_values=[-9999],     # -9999 pasa a ser NaN
                 index_col = 0,         # Índice de DataFrame
                 low_memory=False)      # Uso para leer múltiples datatypes
print('Lectura de datos realizada en:',round(time.process_time() - inicio, 1),
      'segundos\n')

# Resumen de todas las estaciones
print('Resumen de todas las estaciones:\n',
      df.iloc[0:14])

# También se pueden sortear estaciones por nombre
df.columns = df.loc['nombre'].values
print('Estaciones sorteadas por nombre')

# Selección según atributo (ej. nombre de estaciones en latitudes -30 y -35)
e_filtradas = df.loc['latitud'][(
    df.loc['latitud'].astype(float)<-30)
    & 
    (df.loc['latitud'].astype(float)>-35)]
print('Estaciones entre latitudes -30 y -35\n',e_filtradas)

# =============================================================================
# Ejemplo Quinta Normal
# =============================================================================
print('\n===============================================================\n\n',
      'Seleccionando estación Quinta Normal Santiago')
qta_n = df['Quinta Normal Santiago'].iloc[14::].astype(float) # Filtro inicial

# Selección por fechas
print('Seleccionando preiodo 1979-01-01 a 2016-12-31')
qta_n = qta_n[(qta_n.index >= '1979-01-01') & (qta_n.index <= '2016-12-31')] 

# Resampleado a frecuencia anual
print('Tranformando índice para resampleado\n')
qta_n.index = pd.to_datetime(qta_n.index)
print('Resampleando datos')
qta_n_s = qta_n.resample('YS').sum()
qta_n = qta_n.resample('YS').max()


def resumen_estadisticas(df):
    print('Resumen de estadisticas')
    media = df.mean()
    mediana = df.median()
    desv = df.std()
    kurtosis = df.kurtosis()
    n_mayores = df.nlargest(10)
    n_menores = df.nsmallest(10)
    
    print('\n############################\n',
          '\nMedia:\t', media,
          '\nMediana:\t', mediana,
          '\nDesvición:\t', desv,
          '\nKurtosis:\t', kurtosis,
          '\n\n10 mayores:\n\t', n_mayores,
          '\n\n10 menores:\n\t', n_menores,
          '\n-----------------------'
          )
    return

# Resumen de estadisticas precipitaciones máximas anuales
print('\n Resampleado de datos a precipitacion anual acumulada')
resumen_estadisticas(qta_n)

print('\n Resampleado de datos a precipitacion anual acumulada')
# Resumen de estadisticas
resumen_estadisticas(qta_n_s)




















































