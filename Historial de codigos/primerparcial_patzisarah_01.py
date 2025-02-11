# -*- coding: utf-8 -*-
"""PrimerParcial-PatziSarah-01.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qWtXxrtggAVH6Ka0fDIy19woKmBGjNrb
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# utilizado para la manipulación de directorios y rutas
import os

# Cálculo científico y vectorial para python
import numpy as np

import pandas as pd

# Libreria para graficos
from matplotlib import pyplot

# le dice a matplotlib que incruste gráficos en el cuaderno
# %matplotlib inline

# Cargamos el dataset
data = pd.read_csv('/content/drive/MyDrive/IA/LaboratoriosOficiales/Lab4-PatziColodroSarahValentina/SDSS_DR18.csv', delimiter=',')
display(data)

print('Dimensiones:', data.shape)
data.sample(n=200)  # Muestra 10 filas al azar del dataset

"""# **Crear Dataset Sintetico**

**Duplicar columnas variando los valores numericos añadiendo ruido**

* Ruido: Es una pequeña variación aleatoria añadida a los valores numéricos para simular nuevos datos o variabilidad.
Ejemplo: si tienes un valor numérico 10 y añades un 2% de ruido, el nuevo valor podría ser algo cercano, como 10.2 o 9.8
* Columnas numéricas: Se les añade ruido porque las variaciones numéricas son razonables (ej. magnitudes de estrellas).
* Columnas categóricas: No se les añade ruido porque representan categorías fijas o identificadores que no pueden cambiar sin perder su significado.
"""

#Duplicar posible codigo
import pandas as pd
import numpy as np

# Cargar dataset para volver sintetico
df_sintetico= pd.read_csv('/content/drive/MyDrive/IA/LaboratoriosOficiales/Lab4-PatziColodroSarahValentina/SDSS_DR18.csv', delimiter=',')


# Definir las columnas numéricas para variar el valor duplicado y categóricas

#lista con las columnas que contienen valores numéricos que serán modificados.
numeric_columns = ['specobjid','ra', 'dec', 'u', 'g', 'r', 'i', 'z', 'petroRad_u', 'petroRad_g',
                   'petroRad_i', 'petroRad_r', 'petroRad_z', 'petroFlux_u', 'petroFlux_g',
                   'petroFlux_i', 'petroFlux_r', 'petroFlux_z', 'petroR50_u', 'petroR50_g',
                   'petroR50_i', 'petroR50_r', 'petroR50_z', 'psfMag_u', 'psfMag_r',
                   'psfMag_g', 'psfMag_i', 'psfMag_z', 'expAB_u', 'expAB_g', 'expAB_r',
                   'expAB_i', 'expAB_z', 'redshift']

#lista con las columnas categóricas que no serán modificadas.
categorical_columns = ['class', 'objid', 'run', 'rerun', 'camcol', 'field',
                       'plate', 'mjd', 'fiberid']

# Generar nuevas filas con variaciones
def add_noise(series, noise_factor=0.02):

    #Añade una pequeña variación al valor original.
    #noise_factor controla la magnitud de la variación.
    return series * (1 + np.random.normal(0, noise_factor, len(series)))

# Genera nuevos datos modificados:crea duplicados modificados de las columnas numéricas
new_data = df_sintetico[numeric_columns].apply(add_noise)

# Se concatena las columnas numéricas modificadas y categóricas originales
new_df_sintetico = pd.concat([new_data, df_sintetico[categorical_columns]], axis=1)

# Se concatena el dataset original con la versión modificada
df_sintetico = pd.concat([df_sintetico, new_df_sintetico], ignore_index=True)

print('Dimensiones:', data.shape)
print('Dimensiones:', df_sintetico.shape)

"""**avg_magnitude:** Se calcula como el promedio de las magnitudes en las bandas psfMag_u, psfMag_g, psfMag_r, psfMag_i, y psfMag_z.
**Comparación:** La magnitud promedio se compara con el umbral de 6.
data['avg_magnitude'] < 6:

Esto resulta en un valor booleano (True o False).
* True: Si la magnitud promedio es menor que 6, el objeto es considerado visible a simple vista.

* False: Si la magnitud promedio es 6 o mayor, el objeto no es visible a simple vista.

**Agregar 5 columnas basadas en las columnas ya existentes**
"""

# Columna booleana indicando si el redshift es mayor a 0.1 (BOOL)
df_sintetico['redshift_alto'] = df_sintetico['redshift'] > 0.1

# promedio de las magnitudes en las bandas (numeros continuos)
df_sintetico['avg_magnitude'] = df_sintetico[['psfMag_u', 'psfMag_g', 'psfMag_r', 'psfMag_i', 'psfMag_z']].mean(axis=1)

# 2. Texto
# Crear columna 'type_of_telescope' que clasifica el tipo de telescopio necesario para observar el objeto (texto)
df_sintetico['type_of_telescope'] = np.where(df_sintetico['avg_magnitude'] < 6, 'amateur',
                                    np.where(df_sintetico['avg_magnitude'] < 16, 'professional', 'space-based'))

# Nueva columna de caracteres combinando los primeros dígitos de las magnitudes 'psfMag' (u, g, r, i, z)
df_sintetico['codigo_magnitudes'] = df_sintetico.apply(lambda row: ''.join([str(row[f'psfMag_{band}'])[0] for band in ['u', 'g', 'r', 'i', 'z']]), axis=1)

def classify_luminosity(magnitude):
    if magnitude < 10:
        return 1  # Very Low
    elif magnitude < 15:
        return 2  # Low
    elif magnitude < 20:
        return 3  # High
    else:
        return 4  # Very High

# Crear una columna que indica la luminosidad basada en la magnitud promedio (Caracteres)
df_sintetico['luminosity_level'] = df_sintetico['avg_magnitude'].apply(classify_luminosity)

# Mostrar las primeras filas para verificar las nuevas columnas
print(df_sintetico.head())

"""**Graficar comparaciones**"""

import matplotlib.pyplot as plt

# Gráfico del dataset original
plt.figure(figsize=(10, 5))
plt.scatter(data['u'], data['g'], alpha=0.5, label='Dataset Original', color='blue')
plt.title('Relación entre u y g - Dataset Original')
plt.xlabel('u (magnitud)')
plt.ylabel('g (magnitud)')
plt.legend()
plt.show()

# Gráfico del dataset duplicado
plt.figure(figsize=(10, 5))
plt.scatter(df_sintetico['u'], df_sintetico['g'], alpha=0.5, color='orange', label='Dataset Sintetico')
plt.title('Relación entre u y g - Dataset Sintetico')
plt.xlabel('u (magnitud)')
plt.ylabel('g (magnitud)')
plt.legend()
plt.show()

print(df_sintetico.dtypes)

# Convertir 'class' a números
df_sintetico['class'], class_unique = pd.factorize(df_sintetico['class'])
print(f'Clases únicas y sus números: {dict(enumerate(class_unique))}')

# Convertir 'type_of_telescope' a números
df_sintetico['type_of_telescope'], telescope_unique = pd.factorize(df_sintetico['type_of_telescope'])
print(f'Tipos de telescopio únicos y sus números: {dict(enumerate(telescope_unique))}')

# Convertir 'redshift_alto' a números
df_sintetico['redshift_alto'], redshift_alto_unique = pd.factorize(df_sintetico['redshift_alto'])
print(f'Tipos de telescopio únicos y sus números: {dict(enumerate(redshift_alto_unique))}')

# Convertir 'codigo_magnitudes' a números
df_sintetico['codigo_magnitudes'], codigo_magnitudes_unique = pd.factorize(df_sintetico['codigo_magnitudes'])
print(f'codigo_magnitudes y sus números: {dict(enumerate(codigo_magnitudes_unique))}')

#Comparativa de dimensiones
print('Dimensiones:', data.shape)
print('Dimensiones:', df_sintetico.shape)
print(df_sintetico.head())

"""# **Separar datos del dataset**"""

#Convierte el dataset de pandas a un array de NumPy
df_sintetico = np.array(df_sintetico)  # Asegúrate de que los datos ya están en formato NumPy

# Seleccionar todas las columnas excepto la 43, esa la elimina (índice 42 en Python)
X = np.delete(df_sintetico, 42, axis=1)

# Seleccionar solo la columna 43
y = df_sintetico[:, 42]

# Imprimir las primeras filas de X y y
print(X[:2])
print(y[:10])

"""**Separar en entrenamiento y prueba**"""

# Especificar el tamaño del conjunto de prueba (20%)
test_size = 0.2

# Asegurar reproducibilidad (equivalente a random_state en sklearn)
np.random.seed(42)

# Crear un array de índices aleatorios para mezclar los datos
indices = np.random.permutation(X.shape[0])

# Determinar el tamaño del conjunto de prueba
test_set_size = int(X.shape[0] * test_size)

# Dividir los índices para entrenamiento y prueba
test_indices = indices[:test_set_size]
train_indices = indices[test_set_size:]

# Crear los conjuntos de entrenamiento y prueba usando indexación
X_train, X_test = X[train_indices], X[test_indices]
y_train, y_test = y[train_indices], y[test_indices]

# Imprimir los tamaños de los conjuntos de entrenamiento y prueba
print("Tamaño del conjunto de entrenamiento:", X_train.shape)
print("Tamaño del conjunto de prueba:", X_test.shape)

"""**Normalizar**"""

def featureNormalize(X):
    # Creamos una copia de X para no alterar el original
    X_norm = X.copy()

    # Inicializamos dos arrays con ceros para almacenar la media y la desviación estándar
    mu = np.zeros(X.shape[1])
    sigma = np.zeros(X.shape[1])

    # Calculamos la media y la desviación estándar para cada columna (característica)
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)

    # Normalizamos X restando la media y dividiendo por la desviación estándar
    epsilon = 1e-8  # Pequeña constante para evitar la división por cero
    X_norm = (X - mu) / (sigma + epsilon)

    # Devolvemos el dataset normalizado, la media y la desviación estándar
    return X_norm, mu, sigma

# Normalizar el conjunto de entrenamiento
X_train_norm, mu, sigma = featureNormalize(X_train)

# Usar la misma media y desviación estándar del conjunto de entrenamiento para normalizar el conjunto de prueba
epsilon = 1e-8  # Pequeña constante para evitar la división por cero
X_test_norm = (X_test - mu) / (sigma + epsilon)


# Imprimimos los resultados para verificar el proceso
print(X_train)  # Imprime el dataset original
print('Media calculada:', mu)  # Imprime la media de cada característica
print('Desviación estándar calculada:', sigma)  # Imprime la desviación estándar de cada característica
print(X_train_norm)  # Imprime el dataset normalizado

print("Conjunto de entrenamiento normalizado:", X_train_norm[:5])  # Muestra los primeros 5 datos normalizados
print("Conjunto de prueba normalizado:", X_test_norm[:5])  # Muestra los primeros 5 datos normalizados de prueba

"""# **Entrenar modelos Regresion Logistica**"""

# Función sigmoide
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Función de coste con regularización
def lrCostFunction(theta, X, y, lambda_):
    m = y.size
    if y.dtype == bool:
        y = y.astype(int)

    h = sigmoid(X.dot(theta.T))
    h = np.clip(h, 1e-15, 1 - 1e-15)  # Asegura que los valores de h estén entre (0, 1)

    temp = theta
    temp[0] = 0  # No regularizar el término de sesgo (bias)

    #clave para la binary cross-entropy J = (1 / m) * np.sum(-y.dot(np.log(h)) - (1 - y).dot(np.log(1 - h))) y (lambda_ / (2 * m)) * np.sum(np.square(temp)) es la regularización ayuda a evitar el sobreajuste
    J = (1 / m) * np.sum(-y.dot(np.log(h)) - (1 - y).dot(np.log(1 - h))) + (lambda_ / (2 * m)) * np.sum(np.square(temp))

    grad = (1 / m) * (h - y).dot(X) + (lambda_ / m) * temp

    return J, grad

# Función de descenso por gradiente
def descensoGradiente(theta, X, y, alpha, num_iters, lambda_):
    m = y.shape[0]
    theta = theta.copy()
    J_history = []

    for i in range(num_iters):
        h = sigmoid(np.dot(X, theta))  # Asegura que X.dot(theta) sea compatible con np.exp
        h = np.clip(h, 1e-15, 1 - 1e-15)  # Evitar valores extremos para la función de coste

        gradient = (1 / m) * X.T.dot(h - y)
        gradient[1:] = gradient[1:] + (lambda_ / m) * theta[1:]
        theta -= alpha * gradient

        J, _ = lrCostFunction(theta, X, y, lambda_)
        J_history.append(J)

    return theta, J_history

def entrenar_regresion_logistica(X, y, num_etiquetas, alpha, num_iters, lambda_):
    m, n = X.shape
    all_theta = np.zeros((num_etiquetas, n))  # Matriz para guardar los parámetros de cada clase
    cost_histories = []  # Lista para almacenar el historial de costos de cada clase

    # Entrenamos un modelo de regresión logística para cada clase
    for c in range(num_etiquetas):
        print(f"Entrenando modelo para la clase {c}...")

        # Crear etiquetas binarizadas (1 para la clase actual, 0 para el resto)
        y_bin = np.where(y == c, 1, 0)

        # Inicializamos los parámetros theta en cero
        initial_theta = np.zeros(n)

        # Usamos la función de descenso por gradiente para entrenar el modelo
        theta, J_history = descensoGradiente(initial_theta, X, y_bin, alpha, num_iters, lambda_)

        # Guardamos los parámetros entrenados para la clase actual
        all_theta[c, :] = theta

        # Guardamos el historial de costos
        cost_histories.append(J_history)

        # Imprimir el coste final para la clase actual
        print(f"Coste final para la clase {c}: {J_history[-1]}")

    return all_theta, cost_histories

# Parámetros iniciales
alpha = 0.1
num_iters = 1000
lambda_ = 0.01
num_clases = 3  # tienes 3 clases

# X es el conjunto de características y y son las etiquetas, ya tienes X y y preparados
# Entrenar el modelo utilizando el conjunto normalizado
all_theta, cost_histories = entrenar_regresion_logistica(X_train_norm, y_train, num_clases, alpha, num_iters, lambda_)

# Graficar los costos
plt.figure(figsize=(8, 6))

# Para cada clase, grafica el costo en función de las iteraciones
for c in range(num_clases):
    plt.plot(range(num_iters), cost_histories[c], label=f'Clase {c}')

plt.xlabel('Iteraciones')
plt.ylabel('Costo')
plt.title('Evolución del costo durante el entrenamiento para cada clase')
plt.legend()
plt.grid(True)
plt.show()