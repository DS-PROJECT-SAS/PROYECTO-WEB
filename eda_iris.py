import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el conjunto de datos Iris desde seaborn
data = sns.load_dataset('iris')

# Ver las primeras filas del conjunto de datos
print("Primeras filas del dataset:")
print(data.head())

# Mostrar estadísticas descriptivas
print("\nDescripción estadística del dataset:")
print(data.describe())

# Boxplot de las características numéricas
plt.figure(figsize=(12, 8))
sns.boxplot(data=data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']])
plt.title("Boxplot de las características del Iris")
plt.show()


