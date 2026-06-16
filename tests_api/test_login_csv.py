import os
import pytest
from pages.login_page import LoginPage
from utils.datos import leer_csv_login, leer_json_productos

# Resolución de rutas absolutas basada en la estructura del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_CSV = os.path.join(BASE_DIR, "datos", "login.csv")
RUTA_JSON = os.path.join(BASE_DIR, "datos", "productos.json")

@pytest.mark.web
# Inyección directa de la lista de tuplas generada por tu función helper
@pytest.mark.parametrize("usuario, clave, debe_funcionar, descripcion", leer_csv_login(RUTA_CSV))
def test_login_data_driven(driver, usuario, clave, debe_funcionar, descripcion):
    login = LoginPage(driver)
    # Extraemos la URL de configuración base desde el JSON usando la otra función helper
    login.navegar_a_login(leer_json_productos(RUTA_JSON)[0].get("url", "https://www.saucedemo.com/"))
    login.login_exitoso(usuario, clave)
    
    if debe_funcionar:
        assert "/inventory.html" in driver.current_url, f"Fallo en caso exitoso: {descripcion}"
    else:
        assert "/inventory.html" not in driver.current_url, f"Fallo en caso de control: {descripcion}"