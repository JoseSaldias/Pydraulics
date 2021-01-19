# Lectura y análisis de datos observacionales

Los datos de precipitación observacionales de la DGA & DMC fueron recopilados por el [CR2](http://www.cr2.cl/)

## Detalle de rutinas
### **examinacion_estaciones.py**
> 
> - Requiere descarga de archivos
> - Usa datos observacionales de precipitación (análogo a otros tipos de datos)
> - Manejo de directorio
> - Lectura y filtro de archivos
> - Estadísticas (media, mediana, máxima)

### **analisis_de_frecuencia.py**
> - Requiere descarga de archivos
> - Usa datos observacionales de precipitación (análogo a otros tipos de datos)
> - Se aplica a precipitaciones diarias máximas anuales de 24h de duración 
> - Utiliza ajustes de la librería Scipy mediante máxima verosimilitud
> - Determina la función de probabilidades con el mínimo estadístico de muestra
> - Permite obtener si se aprueba o rechaza la hipótesis nula

