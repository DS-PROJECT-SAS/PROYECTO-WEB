#import pytest
#from app import app
#import os
#import csv

#@pytest.fixture
#def client():
#   app.config['TESTING'] = True
#    client = app.test_client()
#   yield client

#def test_formulario_visible(client):
#    """Prueba funcional: Verifica que la página principal carga correctamente."""
#    response = client.get('/')
#    assert response.status_code == 200
#    assert b'RUEDA DE LA VIDA' in response.data

#def test_guardar_datos(client):
#    """Prueba funcional: Enviar datos válidos al formulario."""
#    datos = {
#        'nombre': 'Juan',
#        'apellido': 'Perez',
#        'edad': '30',
#        'salud': '8',
#        'dinero': '7',
#        'carrera': '9',
#        'familia': '6',
#        'amor': '7',
#        'amigos': '8',
#        'diversion': '9',
#        'crecimiento': '7'
#    }

#    response = client.post('/guardar', data=datos, follow_redirects=True)
#    assert response.status_code == 200

#def test_ver_registros(client):
#    """Prueba de aceptación: El historial muestra registros guardados."""
#    response = client.get('/registros')
#    assert response.status_code == 200
#    assert b'Registros disponibles' in response.data
#    assert b'Juan' in response.data  # Verifica que aparece el nombre guardado

import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_grafico_individual(client):
    # Paso 1: Registrar un nuevo usuario con datos válidos
    datos = {
        'nombre': 'Ana',
        'apellido': 'López',
        'edad': '28',
        'salud': '7',
        'dinero': '6',
        'carrera': '8',
        'familia': '9',
        'amor': '6',
        'amigos': '8',
        'diversion': '7',
        'crecimiento': '9'
    }

    response = client.post('/guardar', data=datos, follow_redirects=True)
    assert response.status_code == 200

    # Paso 2: Generar gráfico del primer registro
    response = client.get('/grafico/0')
    assert response.status_code == 200
    assert response.mimetype == 'image/png'








