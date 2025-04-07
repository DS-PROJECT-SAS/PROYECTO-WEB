import pandas as pd
import matplotlib.pyplot as plt

# Datos de empleados y satisfacción
data = {
    'Empleado': ['Ana', 'Luis', 'Carlos'],
    'Satisfacción': [7, 8, 5],
    'Áreas de mejora': ['Comunicación', 'Gestión del tiempo', 'Liderazgo']
}

# Crear el DataFrame
df = pd.DataFrame(data)

# Extraer columnas necesarias
empleados = df['Empleado']
satisfaccion = df['Satisfacción']

# --- Gráfico de barras ---
plt.bar(empleados, satisfaccion, color='blue')
plt.title('Nivel de Satisfacción de los Empleados')
plt.xlabel('Empleado')
plt.ylabel('Satisfacción')
plt.ylim(0, 10)  # Escala de 0 a 10
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# --- Gráfico de líneas ---
plt.plot(empleados, satisfaccion, marker='o', color='green', linestyle='-')
plt.title('Satisfacción de los Empleados a lo largo del tiempo')
plt.xlabel('Empleado')
plt.ylabel('Satisfacción')
plt.ylim(0, 10)
plt.grid(True)
plt.show()
