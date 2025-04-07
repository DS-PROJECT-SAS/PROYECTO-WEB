import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Cargar el dataset Iris
data = sns.load_dataset('iris')

# Mostrar las primeras filas
print("Primeras filas del dataset:")
print(data.head())

# Variables predictoras
X = data[['sepal_length', 'sepal_width', 'petal_width']]

# Variable objetivo
y = data['petal_length']

# Dividir en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Tamaño del conjunto de entrenamiento:", X_train.shape)
print("Tamaño del conjunto de prueba:", X_test.shape)

# Crear el modelo
model = LinearRegression()

# Entrenar el modelo
model.fit(X_train, y_train)

# Mostrar coeficientes
print(f"Coeficientes: {model.coef_}")
print(f"Intersección (intercepto): {model.intercept_}")

# Predicciones
y_pred = model.predict(X_test)

# Comparar valores reales vs predicciones
predictions_df = pd.DataFrame({
    'Real': y_test,
    'Predicción': y_pred
})

print("Comparación entre valores reales y predicciones:")
print(predictions_df.head())

# Calcular métricas
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nError cuadrático medio (MSE): {mse:.4f}")
print(f"Coeficiente de determinación R²: {r2:.4f}")

# Visualización: valores reales vs predichos
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', label='Predicciones')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
         color='red', linewidth=2, label="Línea de referencia")
plt.xlabel("Valores reales")
plt.ylabel("Predicciones")
plt.title("Valores reales vs Predicciones")
plt.legend()
plt.grid(True)
plt.show()

