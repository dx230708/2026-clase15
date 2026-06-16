import pytest
from utils.api_utils import get_users_api

@pytest.mark.api
def test_verificar_estructura_usuarios():
    """Valida que cada usuario del listado contenga los campos requeridos y el formato del avatar."""
    
    respuesta = get_users_api(page=1)
    
    # Validamos éxito de la petición
    assert respuesta.status_code == 200, f"Se esperaba 200 pero se obtuvo {respuesta.status_code}"
    
    json_datos = respuesta.json()
    
    # Validamos que el campo 'data' exista y sea una lista
    assert "data" in json_datos, "El JSON de respuesta no contiene el campo raíz 'data'"
    usuarios = json_datos["data"]
    assert len(usuarios) > 0, "La lista de usuarios está vacía"
    
    # Validamos cada usuario individualmente
    for usuario in usuarios:
        # Criterio principal: Presencia de las claves obligatorias
        claves_requeridas = ["id", "email", "first_name", "last_name"]
        for clave in claves_requeridas:
            assert clave in usuario, f"El usuario con ID {usuario.get('id', 'Desconocido')} no tiene la clave '{clave}'"
            
        # Criterio Extra: Validar que el avatar termine en .jpg
        assert "avatar" in usuario, "El usuario no contiene el campo 'avatar'"
        url_avatar = usuario["avatar"]
        assert url_avatar.lower().endswith(".jpg"), f"El avatar '{url_avatar}' no termina en .jpg"