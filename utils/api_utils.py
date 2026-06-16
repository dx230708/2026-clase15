from datetime import datetime

class MockResponse:
    """Clase auxiliar para emular el comportamiento de una respuesta de requests."""
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def login_api(email, password=None):
    """
    Simula la respuesta del endpoint de login (/api/login)
    para validar la lógica Data-Driven sin depender de restricciones de red.
    """
    # Escenario de Éxito: Tiene email válido y password
    if email == "eve.holt@reqres.in" and password == "cityslicka":
        return MockResponse(
            json_data={"token": "QpwL5tke4Pnpja7X4"}, 
            status_code=200
        )
    
    # Escenario de Falla: Falta el password
    elif email == "eve.holt@reqres.in" and password is None:
        return MockResponse(
            json_data={"error": "Missing password"}, 
            status_code=400
        )
    
    # Cualquier otro caso de control genérico (Credenciales incorrectas)
    else:
        return MockResponse(
            json_data={"error": "user not found"}, 
            status_code=400
        )

def get_users_api(page=1):
    """
    Simula la respuesta del endpoint GET /api/users?page=1
    con un listado de usuarios estructurado para validar esquemas y extensiones.
    """
    if page == 1:
        datos_usuarios = [
            {
                "id": 1,
                "email": "george.bluth@reqres.in",
                "first_name": "George",
                "last_name": "Bluth",
                "avatar": "https://reqres.in/img/faces/1-image.jpg"
            },
            {
                "id": 2,
                "email": "janet.weaver@reqres.in",
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://reqres.in/img/faces/2-image.jpg"
            }
        ]
        return MockResponse(json_data={"page": 1, "data": datos_usuarios}, status_code=200)
    
    return MockResponse(json_data={"page": page, "data": []}, status_code=200)

def create_user_api(name, job):
    """
    Simula la respuesta del endpoint POST /api/users
    retornando un entorno con ID dinámico y timestamp con el año actual.
    """
    # Obtenemos la fecha actual en formato ISO 8601 típico de APIs (Ej: 2026-06-15T23:20:44.000Z)
    fecha_actual_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    payload_respuesta = {
        "name": name,
        "job": job,
        "id": "251",
        "createdAt": fecha_actual_iso
    }
    
    return MockResponse(json_data=payload_respuesta, status_code=201)