# -*- coding: utf-8 -*-
""" Descripción
Análisis de frecuencia anual precipitaciones de 24h de duración
Archivos compilados de datos observacionales CR2 

Sitio web: http://www.cr2.cl/datos-de-precipitacion/
Archivo: cr2_prDaily_2018_ghcn.zip

José Ignacio Saldías 
jose.saldias@cigiden.cl
"""

# Incluidas en python
import warnings

# Instaladas a través de Anaconda
import pandas as pd
import numpy as np
import scipy.stats as ss

# =============================================================================
# Se recomienda la lectura previa del archivo "examinacion_estaciones.py"
# =============================================================================

def mejor_distribucion(data, DISTRIBUTIONS):
    """
    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame de una estacion en particular datetimeindex, dato
    DISTRIBUTIONS : ss.distribution
        lista de distribuciones de la librería scipy

    Returns
    -------
    best_distribution : ss.distribution
        distribucion de la libreria scipy que mejor ajusta en base al test
    best_chi : float
        mínimo valor del test chi cuadrado
    chi_estadistico : float
        estadistico de comparación en base a los grados de libertad

    """
    
    # Histograma de datos observados
    bins = int(np.floor(5*np.log10(len(data)))+1)
    y, x = np.histogram(data, bins=bins)
    
    # Para cada una de las distribuciones
    for distribution in DISTRIBUTIONS:
        try:
            # Ignorar advertencias de valores que no se pueden ajustar
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                
                # Ajuste de distribución
                params = distribution.fit(data)
                
                # Separar parámetros de escala, forma, localización y otros
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]
                
                # Valores esperados
                esperado = []
                for k in range(len(x)-1):
                    li = distribution.cdf(x[k], loc=loc, scale=scale, *arg)
                    ls = distribution.cdf(x[k+1], loc=loc, scale=scale, *arg)
                    esperado.append((ls - li)*len(data))
                esperado = np.array(esperado)
                
                # Test Estadistico
                chi_muestral = (((y-esperado)**2)/esperado).sum()
                grados_de_libertad = bins-len(params)-1
                alpha = 0.05
                chi_estadistico = ss.chi2.ppf(1 - alpha, grados_de_libertad)
                
                # Poner la primera distribución como la mejor
                if distribution == DISTRIBUTIONS[0]:
                    best_distribution = distribution
                    best_chi = chi_muestral
                
                # Identificar distribución con menor estadistico de muestra
                if  best_chi > chi_muestral:
                    best_distribution = distribution
                    best_chi = chi_muestral
        
        except Exception:
            pass
        
    return (best_distribution, best_chi, chi_estadistico)


# Archivo se necesita descargar (cr2.cl)
n_archivo = 'cr2_prDaily_2018_ghcn.txt'

df = pd.read_csv(
    n_archivo,
    index_col = 0,
    skiprows = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    na_values = (-9999)
    )['Quinta Normal Santiago'] # nombre de estacion, revisar csv

# Resampleo
df.index = pd.to_datetime(df.index.values)
df = df.resample('YS').max().dropna()

# distribuciones a ajustar
distribuciones = [ss.gumbel_r, ss.pearson3, ss.lognorm, ss.rayleigh,
                  ss.invgamma, ss.loggamma]

#resultados de ajuste
dist, chi_e, chi_m = mejor_distribucion(df, distribuciones)
