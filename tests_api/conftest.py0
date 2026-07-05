import os
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.fixture
def driver():
    """Inicializa Chrome de forma nativa sin requerir webdriver_manager externamente."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Descomentar si corrés en entornos CI/CD sin interfaz
    
    # En Selenium 4+, instanciar así busca el driver local de forma automática
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    
    yield driver
    driver.quit()

@pytest.fixture
def usuario_logueado(driver):
    """Realiza el login automático antes de los flujos de negocio."""
    url_base = "https://www.saucedemo.com/"
    usuario = "standard_user"
    clave = "secret_sauce"
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    login_page.navegar_a_login(url_base)
    login_page.login_exitoso(usuario, clave)
    
    return driver, inventory_page

def pytest_make_parametrize_id(config, val, argname):
    """Fuerza a Pytest a renderizar strings con caracteres especiales de forma legible."""
    if isinstance(val, str):
        return val.encode('utf-8').decode('utf-8')
    return None