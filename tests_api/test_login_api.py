import pytest
from utils.api_utils import login_api

@pytest.mark.api  # <--- Marcado como API
@pytest.mark.parametrize(
    "email, password, status_esperado, requiere_token",
    [
        # Caso 1: Datos válidos (Debe retornar 200 y un token)
        ("eve.holt@reqres.in", "cityslicka", 200, True),
        # Caso 2: Datos inválidos - Email sin password (Debe retornar 400)
        ("eve.holt@reqres.in", None, 400, False)
    ]
)
def test_login_endpoint(email, password, status_esperado, requiere_token):
    """Valida el comportamiento del login de la API ante credenciales válidas e inválidas."""
    
    # Ejecutamos la petición a través de nuestro utilitario
    respuesta = login_api(email, password)
    
    # Validamos el código de estado HTTP
    assert respuesta.status_code == status_esperado, \
        f"Se esperaba status {status_esperado} pero se obtuvo {respuesta.status_code}"
    
    # Validaciones de la estructura del JSON de respuesta
    json_datos = respuesta.json()
    if requiere_token:
        assert "token" in json_datos, "La respuesta exitosa no contiene el campo 'token'"
        assert len(json_datos["token"]) > 0, "El token devuelto está vacío"
    else:
        assert "error" in json_datos, "La respuesta de falla no contiene el campo 'error'"
        assert json_datos["error"] == "Missing password", "El mensaje de error no es el esperado"