'''
Consider earthquakes in Mexico since (January 1st 1950) 
and make the preprocessing of the data: Handling missing values, 
(magnitude,Depth, Latitude, Longitude).

'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Cargar la base de datos
df = pd.read_csv('Tareas/dataSets/SSNMX_catalogo_19500101_20240205.csv', skiprows=4, skipfooter=7, engine='python')

# Convertir columnas a numéricas
df['Magnitud'] = pd.to_numeric(df['Magnitud'], errors='coerce')
df['Profundidad'] = pd.to_numeric(df['Profundidad'], errors='coerce')
df['Latitud'] = pd.to_numeric(df['Latitud'], errors='coerce')
df['Longitud'] = pd.to_numeric(df['Longitud'], errors='coerce')

# Verificar si hay valores faltantes en magnitud, profundidad, latitud y longitud
valores_nan = df[['Magnitud', 'Profundidad', 'Latitud', 'Longitud']].isnull().sum()
print(f"Valores faltantes en cada columna:\n{valores_nan}")

# Grafica de los datos 
im = plt.imread('Tareas/mapa.jpg')
fig, ax = plt.subplots(figsize=(15, 15))
im = ax.imshow(im, extent=[-120, -84, 14, 34])
ax.scatter(df['Longitud'], df['Latitud'], color='red', marker='o', alpha=0.1)
x = np.linspace(-120, -84, 100000)
ax.plot(x, (-0.6) * (x + 117) + 33, color="blue")
region_a = df[df['Latitud'] > (-0.6) * (df['Longitud'] + 117) + 33]
region_b = df[df['Latitud'] <= -0.6 * (df['Longitud'] + 117) + 33]
ax.scatter(region_a['Longitud'], region_a['Latitud'], color='magenta', alpha=0.3, marker='o')
ax.scatter(region_b['Longitud'], region_b['Latitud'], color='green', alpha=0.3, marker='o')
ax.set_xlim([-120, -84])
ax.set_ylim([14, 34])
plt.show()

## se obtienen los promedios 
print(f'Promedio de la region A: {region_a["Magnitud"].mean()}')
print(f'Promedio de la region B: {region_b["Magnitud"].mean()}')
promedio_a = region_a['Magnitud'].mean()
promedio_b = region_b['Magnitud'].mean()

# sustitucion de los datos NaN en Magnitud con los promedios de las regiones A y B
df.loc[df['Latitud'] > (-0.6) * (df['Longitud'] + 117) + 33, 'Magnitud'] = df.loc[
    df['Latitud'] > (-0.6) * (df['Longitud'] + 117) + 33, 'Magnitud'].fillna(promedio_a)
df.loc[df['Latitud'] <= -0.6 * (df['Longitud'] + 117) + 33, 'Magnitud'] = df.loc[
    df['Latitud'] <= -0.6 * (df['Longitud'] + 117) + 33, 'Magnitud'].fillna(promedio_b)

# Verificar nuevamente si hay valores faltantes en Magnitud
valoresNanDespues = df['Magnitud'].isnull().sum()
print(f"Valores faltantes en la columna 'Magnitud' después de la sustitución:\n{valoresNanDespues}")

# Suponemos que los datos faltantes son las réplicas del terremoto anterior por lo que lo más conveniente 
# es elegir el dato anterior 
df['Profundidad'] = df['Profundidad'].fillna(method='ffill')

# Verificar nuevamente si hay valores faltantes en Profundidad
valoresNanProfundidadDespues = df['Profundidad'].isnull().sum()
print(f"Valores faltantes en la columna 'Profundidad' después de la sustitución:\n{valoresNanProfundidadDespues}")

# Verificar nuevamente si hay valores faltantes 
valores_nan = df[['Magnitud', 'Profundidad', 'Latitud', 'Longitud']].isnull().sum()
print(f"Valores faltantes en cada columna:\n{valores_nan}")
