from flask import Flask, render_template, request, redirect, send_file, render_template_string
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

CAMPOS_PERSONALES = ['nombre', 'apellido', 'edad']

CATEGORIAS = [
    'salud', 'dinero', 'carrera', 'familia',
    'amor', 'amigos', 'diversion', 'crecimiento'
]

PREGUNTAS = {
    'salud': '¿Cómo te sientes físicamente?',
    'dinero': '¿Estás satisfecho con tu situación financiera?',
    'carrera': '¿Te sientes realizado profesionalmente?',
    'familia': '¿Tienes una buena relación con tu familia?',
    'amor': '¿Cómo está tu vida amorosa?',
    'amigos': '¿Tienes amigos en quienes confiar?',
    'diversion': '¿Disfrutas tiempo para ti y tus hobbies?',
    'crecimiento': '¿Estás aprendiendo y creciendo personalmente?'
}

@app.route('/')
def index():
    return render_template('formulario.html', categorias=CATEGORIAS, preguntas=PREGUNTAS)

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = {campo: request.form[campo] for campo in CAMPOS_PERSONALES}
    datos.update({categoria: request.form[categoria] for categoria in CATEGORIAS})

    columnas = CAMPOS_PERSONALES + CATEGORIAS

    with open('datos_rueda.csv', mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=columnas)
        
        archivo.seek(0, 2)
        if archivo.tell() == 0:
            writer.writeheader()

        writer.writerow(datos)

    return redirect('/')


@app.route('/grafico')
def mostrar_grafico():
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')
    if df.empty:
        return 'No hay datos aún.'

    datos = df[CATEGORIAS].iloc[-1]
    categorias = list(datos.index)
    valores = datos.values.astype(float).tolist()
    valores += valores[:1]
    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angulos, valores, color='blue', linewidth=2)
    ax.fill(angulos, valores, color='skyblue', alpha=0.4)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias)
    ax.set_yticks(range(1, 11))
    ax.set_title("Rueda de la Vida (último registro)", size=16, y=1.1)

    ruta_imagen = 'static/grafico.png'
    os.makedirs('static', exist_ok=True)
    plt.savefig(ruta_imagen)
    plt.close()

    return send_file(ruta_imagen, mimetype='image/png')


@app.route('/registros')
def ver_registros():
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')
    if df.empty:
        return 'No hay datos aún.'

    promedios = df[CATEGORIAS].mean().round(2).to_dict()
    registros = df.to_dict(orient='records')

    return render_template_string('''
    <html>
    <head><title>Registros guardados</title></head>
    <link rel="stylesheet" href="/static/css/registros.css">
    <body>
        <h2>Preguntas por categoría</h2>
        <ul>
        {% for categoria in categorias %}
            <li><b>{{ categoria.capitalize() }}</b>: {{ preguntas[categoria] }}</li>
        {% endfor %}
        </ul>

        <h2>Promedio por categoría</h2>
        <ul>
        {% for categoria, valor in promedios.items() %}
            <li><b>{{ categoria.capitalize() }}</b>: {{ valor }}</li>
        {% endfor %}
        </ul>

<h2>Registros disponibles</h2>
<table border="1">
    <tr>
        {% for key in registros[0].keys() %}
            <th>{{ key.capitalize() }}</th>
        {% endfor %}
        <th>Ver gráfico</th>
        <th>Editar</th>
        <th>Eliminar</th>
    </tr>
    {% for fila in registros %}
    {% set idx = loop.index0 %}
    <tr>
        {% for valor in fila.values() %}
            <td>{{ valor }}</td>
        {% endfor %}
        <td><a href="/grafico/{{ idx }}">Ver</a></td>
        <td><a href="/editar/{{ idx }}">Editar</a></td>
        <td><a href="/eliminar/{{ idx }}" onclick="return confirm('¿Estás seguro de eliminar este registro?')">Eliminar</a></td>
    </tr>
    {% endfor %}
</table>


        <br><a href="/">← Volver al formulario</a>
    </body>
    </html>
    ''', registros=registros, promedios=promedios, categorias=CATEGORIAS, preguntas=PREGUNTAS)


@app.route('/grafico/<int:indice>')
def mostrar_grafico_individual(indice):
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')
    if df.empty or indice >= len(df):
        return 'Registro no encontrado.'

    datos = df.iloc[indice]

    # Obtener nombre y apellido del registro
    nombre = datos.get('nombre', 'Desconocido')
    apellido = datos.get('apellido', '')

    # Solo categorías, eliminando campos personales
    categorias = [col for col in datos.index if col not in ['nombre', 'apellido', 'edad']]
    valores = datos[categorias].values.astype(float).tolist()
    valores += valores[:1]

    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angulos, valores, color='green', linewidth=2)
    ax.fill(angulos, valores, color='lime', alpha=0.4)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias)
    ax.set_yticks(range(1, 11))
    
    # ✅ TÍTULO personalizado con el nombre
    ax.set_title(f"Rueda de la Vida - {nombre} {apellido}", size=14, y=1.1)

    ruta_imagen = f'static/grafico_{indice}.png'
    os.makedirs('static', exist_ok=True)
    plt.savefig(ruta_imagen)
    plt.close()

    return send_file(ruta_imagen, mimetype='image/png')

@app.route('/editar/<int:indice>', methods=['GET', 'POST'])
def editar(indice):
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')

    if indice >= len(df):
        return 'Registro no encontrado.'

    if request.method == 'POST':
        for campo in df.columns:
            df.at[indice, campo] = request.form[campo]
        df.to_csv('datos_rueda.csv', index=False)
        return redirect('/registros')

    datos = df.iloc[indice].to_dict()
    return render_template_string('''
        <h2>Editar Registro</h2>
        <form method="POST">
            {% for campo, valor in datos.items() %}
                <label>{{ campo.capitalize() }}:</label>
                <input type="{{ 'number' if campo in categorias else 'text' }}" name="{{ campo }}" value="{{ valor }}" required><br><br>
            {% endfor %}
            <button type="submit">Guardar cambios</button>
            <a href="/registros"><button type="button">Cancelar</button></a>
        </form>
    ''', datos=datos, categorias=CATEGORIAS)


@app.route('/eliminar/<int:indice>')
def eliminar(indice):
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')

    if indice >= len(df):
        return 'Registro no encontrado.'

    df = df.drop(index=indice).reset_index(drop=True)
    df.to_csv('datos_rueda.csv', index=False)

    return redirect('/registros')


if __name__ == '__main__':
    app.run(debug=True)





