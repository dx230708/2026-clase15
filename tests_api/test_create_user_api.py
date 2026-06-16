import pytest
from datetime import datetime
from utils.api_utils import create_user_api

@pytest.mark.api
@pytest.mark.parametrize(
    "nombre, trabajo",
    [
        ("Alejandro", "QA Automation Engineer"),
        ("Matias", "DevOps Specialist"),
        ("Laura", "Technical Lead")
    ]
)
def test_creacion_usuarios_parametrizado(nombre, trabajo):
    """Valida que el alta de usuarios retorne 201 y la fecha de creación corresponda al año en curso."""
    
    respuesta = create_user_api(nombre, trabajo)
    
    # 1. Comprobamos código de estado 201 Created
    assert respuesta.status_code == 201, f"Se esperaba status 201 pero se obtuvo {respuesta.status_code}"
    
    json_datos = respuesta.json()
    
    # 2. Verificamos que los datos devueltos coincidan con lo enviado
    assert json_datos["name"] == nombre, f"El nombre '{json_datos['name']}' no coincide con el enviado '{nombre}'"
    assert json_datos["job"] == trabajo, f"El puesto '{json_datos['job']}' no coincide con el enviado '{trabajo}'"
    
    # 3. Comprobamos que exista el ID de recurso creado
    assert "id" in json_datos, "La respuesta no incluyó el 'id' del nuevo usuario"
    
    # 4. Comprobamos que 'createdAt' incluya el año actual de forma dinámica
    assert "createdAt" in json_datos, "La respuesta no incluyó el campo 'createdAt'"
    
    anio_actual = str(datetime.now().year) # Extrae "2026"
    fecha_creacion = json_datos["createdAt"]
    
    assert anio_actual in fecha_creacion, \
        f"La fecha de creación '{fecha_creacion}' no contiene el año actual '{anio_actual}'"