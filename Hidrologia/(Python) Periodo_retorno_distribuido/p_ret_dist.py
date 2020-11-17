# -*- coding: utf-8 -*-
"""
José Ignacio Saldías (jose.saldias@cigiden.cl) 
Nov 2020

Rutina de generación para mapa de periodo de retorno distribuido en la
cuenca rio maipo.

"""

# Modulos utilizados
import os
import warnings

# Utilizados en distribución anaconda
import pandas as pd
import scipy.stats as ss
import numpy as np

# Intalación adicional
import xarray as xr  # conda install xarray
import fiona         # anaconda.org/conda-forge/fiona
from shapely.geometry import Point, Polygon # anaconda.org/conda-forge/shapely
import rasterio      # https://anaconda.org/conda-forge/rasterio



print('\nLeyendo rutas de archivos\n')
# Inicio De rutina
# =============================================================================
# Archivos necesarios y su ubicación relativa:
#     
#     Datos de precipitación observacionales:
#         ~\cr2_prDaily_2018_ghcn.txt -> Estaciones DGA, DMC Chile
#
#     Datos de precipitacion simulados/interpolados:
#         ~\CR2MET_005deg_Antiguo.nc -> producto grillado observacional Cr2
#
#     Datos espaciales:
#         ~\Shapefile\cl_cuencas_hidrograficas_geoPolygon.shp -> Cuencas Chile
#         ~\Shapefile\'Poligonos de voronoi Cuenca Rio maipo.shp'
# =============================================================================

# Manejo de directorio
root_folder = os.getcwd() # Directorio local
ruta_archivo_nc = r'CR2MET_005deg_Antiguo.nc'
ruta_datos = os.path.join(root_folder, r'cr2_prDaily_2018_ghcn.txt')
ruta_shapefile_cuencas = os.path.join(
    root_folder,r'Shapefile', r'cl_cuencas_hidrograficas_geoPolygon.shp')

ruta_poligonos =  os.path.join(
    root_folder, r'Shapefile', r'Poligonos de voronoi Cuenca Rio maipo.shp')


# Lectura de Archivos
# =============================================================================
# Lectura de archivos de precipitación observacional con pandas DataFrame y
# apertura de shapefile y extracción de coordenadas de dominio a un 
# polígono con los módulos shapely y fiona
# =============================================================================

print('Leyendo Datos de precipitacion\n')
# Datos de precipitacion
df = pd.read_csv(ruta_datos, na_values=[-9999], index_col = 0,
                 low_memory=False)

print('Recopilando datos espaciales de \n \t {}\n'.format(
    ruta_shapefile_cuencas))
# Datos espaciales de dominio
with fiona.open(ruta_shapefile_cuencas, "r") as shapefile: # apertura shp
	maipo = shapefile[78]                                  # n° 78
coords = maipo['geometry']['coordinates'][0]               
zona_maipo = Polygon(coords)                        # Asignacion coordenadas


# Selección de estaciones en el dominio
# =============================================================================
# Se recorre estación por estación del DataFrame de precipitaciones con ciclo
# for tomando las coordenadas de latitud y longitud y se ve si está en el 
# polígono (dominio). Luego, estas estaciones son separadas y se exportan los
# datos con su código de estación, nombre y cantidad de años con datos
# =============================================================================

est_en_dom = [] # vector de almacenamiento de estaciones en dominio

for i in range(len(df.columns)):            # i = 1 ... n° estaciones
	lat = df[df.columns[i]].loc['latitud']  # Latitud estación i
	lon = df[df.columns[i]].loc['longitud'] # Longitud estación i
	geom = Point(float(lon),float(lat))     # Conversión obejeto shapely
	en_dom = geom.within(zona_maipo)        # Verificación de punto en dominio
	if en_dom:
		est_en_dom.append(df.columns[i])    # Guardado de punto en vector
	else:
		next
	
estaciones = df[[*est_en_dom]]  # Dataframe de estaciones dentro del dominio

e_nom = [] # Almacenamiento de nombre
e_cod = [] # Almacenamiento de codigo
e_nd = []  # Almacenamiento de numero de años con datos

# Filtro de estaciones segun los años de datos que tenga
for j in range(len(estaciones.columns)):   # j = 1 .. n° estaciones en dominio
	codigo = estaciones.columns[j]
	nombre = estaciones[estaciones.columns[j]].loc['nombre']
	pr = estaciones[estaciones.columns[j]][14::].dropna() # datos estacion j
	pr.index = pd.to_datetime(pr.index)
	n_datos = len(pr)//365
	if n_datos > 30:
		e_nom.append(nombre)      # Guardado de nombre
		e_cod.append(codigo)      # Guardado de codigo
		e_nd.append(n_datos)      # Guardado de años con dato (>30)
	else:
		next

# Asignación de DataFrame con datos de estaciones a variable
df_est = pd.DataFrame({'Nombre':e_nom,'Codigo Estacion':e_cod,'n datos': e_nd})

# Exportar los datos a directorio local
df_est.to_csv('Estaciones dentro del dominio.csv') 
print('Estaciones dentro del dominio: {}\n'.format(df_est))



# Ajuste de mejor función de densidad para cada estación
# =============================================================================
# Se crea la función mejor_distribucion que encuentra el ajuste mediante
# método de máxima verosimilitud que con menor EMC con los datos observados
#
# La rutina se basa en el ejemplo de "tmthydvnprt" https://stackoverflow.com/
# questions/6620471/fitting-empirical-distribution-to-theoretical-ones-with-
# scipy-python 
# =============================================================================

# Create models from data
def mejor_distribucion(data, DISTRIBUTIONS):
    """
    Toma la lista DISTRIBUTIONS y la ajusta a datos

    Parameters
    ----------
    data : pandas dataframe
        Datos observacionales
    DISTRIBUTIONS : 
        Funciones del módulo scipy (scipy.stats._continuous_distns)

    Returns
    -------
    best_distribution.name: String
        Nombre de la distribución scipy.stat que mejor ajusta
    best_params : TYPE
        Parámetros de la de distribución

    """
    # Histograma de datos observados
    bins = int(np.floor(5*np.log10(len(data)))+1)
    y, x = np.histogram(data, bins=bins, density=True)
    
	# Puntos medios de las clases
    x = (x + np.roll(x, -1))[:-1] / 2.0
    
    # Para cada una de las distribuciones
    for distribution in DISTRIBUTIONS:
        
        # Tratar de encontrar la distribución
        try:
            # Ignorar advertencias de valors que no se pueden ajustar
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                
                # Ajuste de distribución
                params = distribution.fit(data)
                
                # Separar parámetros de escala, forma, localización y otros
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                pdf_emp = y
                
                # Error cuadrático
                sqe = np.sum(np.power(pdf_emp - pdf, 2.0))
                
                # Poner la primera distribución como la mejor
                if distribution == DISTRIBUTIONS[0]:
                    best_distribution = distribution
                    best_params = params
                    best_sqe = sqe
                
                # Identificar cual distribución tiene menor error
                if best_sqe > sqe > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sqe = sqe
        
        except Exception:
            pass
        
    return (best_distribution.name, best_params)

# Datos de estaciones en dominio
estaciones = df_est['Nombre'].values
df2 = df[df_est['Codigo Estacion']].iloc[14:]
df2.index = pd.to_datetime(df2.index)

# Lista de distribuciones a ajustar
distribuciones =[ss.gumbel_r, ss.pearson3, ss.gamma, ss.invweibull,
                 ss.loggamma, ss.lognorm, ss.genextreme, ss.rayleigh]

# Diccionario donde guardar nombre de estación y distribución
funcion_por_estacion = {}

print('Ajustando las distribuciones {} \n'.format(
    [i.name for i in distribuciones]))
for i in range(len(estaciones)):
    
    # Resampleamos DataFrame a máximos anuales
    df2[df2.columns[i]] = df2[df2.columns[i]].astype(float) # Datatype
    dfy = df2[df2.columns[i]].resample('YS').max().dropna() # Resampleo
    nombre = estaciones[i]
    datos = dfy.values
 
    # Obtener la distribución con mejor ajuste
    cdf_emp = (np.arange(len(datos))+1)/(len(datos)+1)      # Curva empírica
    nombre_dist, params_dist = mejor_distribucion(datos, distribuciones)

    funcion_por_estacion[nombre] = [nombre_dist] # Almacenamiento distribucion

# Exportar datos de distribuciones según estación
pd.DataFrame(funcion_por_estacion).to_csv('funciones segun estacion.csv')


# Procesamiento archivos NetCDF (.nc)
# =============================================================================
# Se recorta el archivo .nc en los cuadrantes respectivos para luego filtrar
# los puntos en el shapefile correspondiente al dominio con la función 
# extraer_xy definida
# =============================================================================

def extraer_xy(shapefile):
    """
    Toma los valores lat y lon de un shapefile y los almacena en un 
    diccionario
    """
    polygons = {}
    
    # Abrir archivo en un ambiente local
    with fiona.open(shapefile, "r") as root_shp:
        
        # Iterar en el shapefile tomando el nombre y polígono
        for shape in root_shp:
            
            try:
                current_name = shape['properties']['Nombre']
                current_polygon = Polygon(shape['geometry']['coordinates'][0])
            
            except:
                current_polygon= Polygon(
                        shape['geometry']['coordinates'][0][0])
                current_name = shape['properties']['Nombre']
            
            # Almacenar el polígono y su nombre
            polygons[shape['id']] = {current_name : current_polygon}
        
    return polygons

def point_check(point,polygons):
    """
    Verifica si un punto está dentro de un diccionario de polígonos y retorna
    el polígono al que pertenece
    """
    # Verifica la estructura del punto
    if type(point) == Point:
        None
    
    else:
        point = Point(point)
    
    # Iterar en los valores hasta encontrar aquel que contenga el punto
    for key in polygons:
        current_polygon = polygons[key]
        
        for subkey in current_polygon:
            check = point.within(current_polygon[subkey])
        
        if check:
            result = True			 
            break
        
        else:
            result = False
            continue
    
    return subkey, result


def set_key(dictionary, key, value):
	""" Introduces value in dictionary or appends to existing key """
	
	# Check if key exists
	if key not in dictionary:
		dictionary[key] = value
	
	# Check data structure 
	elif type(dictionary[key]) == list:
		dictionary[key].append(value)
	
	# Add as a list if not
	else:
		dictionary[key] = [dictionary[key], value]


# Dataset
ds = xr.open_dataset(ruta_archivo_nc)

# Acotación de dominio
print('Procesando archivos NetCDF')
clip = ds.isel(lat = slice(440, 500), lon = slice(99, 150))
lat = clip.coords['lat'].values         # Valores de latitud
lon = clip.coords['lon'].values         # Valores de longitud

# Extraccion geometría de polígonos
poligonos = extraer_xy(ruta_poligonos)

# Funciones de distribución por polígonos
funciones = pd.DataFrame(funcion_por_estacion)

# For construcction & debug
warnings.filterwarnings("ignore")

# Condiciones iniciales
evento = 65 # Magnitud de precipitación en mm
periodo_de_retorno = 10 # Periodo de retorno en años
print('Magnitud de precipitación para generación de periodo de retorno {} años\
      \n'.format(evento))

# Diccionario para guardar resultados
resultados_probabilidad = {}
resultados_magnitud = {}
X, Y = np.meshgrid(-lon, lat)
Z = X-X

# Para cada punto
for i in range(len(lon)):
    x = lon[i]
    print('longitud actual:', str(round(x, 3)),
          '(' + str(i + 1) + '/' + str(len(lon)) + ')')
    
    for j in range(len(lat)):
        y = lat[j]
        # Verificar si el punto está en el dominio y su distribución
        location , result = point_check(Point(x,y), poligonos)
		
		# Ajustar parámetros para puntos dentro del dominio
		
        if result:
            try:
                # Atributos de la distribución en el punto
                distribution = getattr(ss, funciones[location].values[0])
                
                # Valores de magnitud en el punto
                pr = clip['pr'][:, j, i]
				
				# Resampleado
                anual_max = pr.resample(time='YS').max()
				
				# Ajuste de distribución correspondiente
                params = distribution.fit(anual_max)
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]
				
				# Return period
                T = 1/(1-distribution.cdf(evento,  loc = loc, scale = scale,
								   *arg))
                Z[j][i] = T
				# Store results
				
                set_key(resultados_probabilidad, 'Point', (y, x))
                set_key(resultados_probabilidad, 'Return Period', T)
                set_key(resultados_probabilidad, 'Distribution',
                                                funciones[location].values[0])
                set_key(resultados_probabilidad, 'Parameters', params)
                set_key(resultados_probabilidad, 'Latitud', y)
                set_key(resultados_probabilidad, 'Longitud', x)

            except:
				
				# Assign point last distribution and nan to return period
				
                set_key(resultados_probabilidad, 'Point', (y,x))
                set_key(resultados_probabilidad, 'Return Period', np.nan)
                set_key(resultados_probabilidad, 'Distribution',
                        						funciones[location].values[0])
                set_key(resultados_probabilidad, 'Parameters', params)
                set_key(resultados_probabilidad, 'Latitud', y)
                set_key(resultados_probabilidad, 'Longitud', x)

# Interpolar puntos que no pueden ser ajustados
results = pd.DataFrame(resultados_probabilidad)
results['Return Period'] = results['Return Period'].interpolate(
		method ='linear', limit_direction = 'backward', limit = 1)

# Grabar como xlsx
print('\nGuardando resultados en "Resultados.xlsx"')
results.to_excel('Resultados.xlsx')


# Creación de raster
# =============================================================================
# Se crea una grilla de resolución con la librería rasterio
# =============================================================================
#%%
res = 0.05                  # Resolucion
transform = rasterio.Affine.translation(
     lon[0] - res / 2, lat[0] - res / 2) * rasterio.Affine.scale(res, res)

name ='Mapa_periodo_de_retorno_{}mm.tif'.format(evento)

print("Guardando en archivo tiff \nNombre: {}".format(name))
# Escritura de raster
with rasterio.open(
    name,                   # Nombre del archivo
    'w',                    # Modo de apertura
    driver='GTiff',         # Driver
    height=Z.shape[0],      # Alto
    width=Z.shape[1],       # Ancho 
    count=1,                # N° de Bandas
    dtype=Z.dtype,          # Tipo de datos
    nodata=0,               # NaN values
    crs='+proj=latlong',    # Sistema de proyeccion
    transform=transform,    # Transformación
) as dst:
    dst.write(Z, 1)         # Escribir raster