import os
import logging
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# -------------------------------------------------------------------------
# CONFIGURACI√ìN DE LOGGING UNIFICADO (Criterio 3)
# -------------------------------------------------------------------------
# Nos aseguramos de que exista la carpeta de logs
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)",
    handlers=[
        logging.FileHandler("logs/suite.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()  # Muestra tambi√©n los logs en la consola
    ]
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------
# FIXTURE DEL WEBDRIVER (INTEGRADO CON LOGS)
# -------------------------------------------------------------------------
@pytest.fixture(scope="function")
def driver(request):
    logger.info(f"Iniciando WebDriver para el test: {request.node.name}")

    options = webdriver.ChromeOptions()
    
    # üöÄ DETECCI√ìN AUTOM√ÅTICA DE CI (GitHub Actions)
    if os.environ.get("CI") == "true":
        logger.info("Entorno CI detectado. Forzando modo Headless para Linux.")
        options.add_argument("--headless=new") # Ejecuci√≥n en segundo plano sin pantalla
        options.add_argument("--no-sandbox")   # Requerido para entornos de contenedores/Linux
        options.add_argument("--disable-dev-shm-usage") # Evita problemas de memoria compartida en Docker/VMs
    else:
        logger.info("Entorno Local detectado. Levantando navegador con interfaz gr√°fica.")
        options.add_argument("--start-maximized")

    # Filtro para evitar el pop-up gris de las contrase√±as que vimos en el laboratorio
    prefs = {
        "profile.password_manager_leak_detection": False,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # Inicializaci√≥n segura
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    
    request.node._driver = driver
    yield driver
    
    logger.info(f"Cerrando WebDriver para el test: {request.node.name}")
    driver.quit()

# -------------------------------------------------------------------------
# HOOKS DE REPORTE HTML Y CAPTURA EN CASO DE FALLO (Criterio 2)
# -------------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Detecta el resultado de cada fase del test e interact√∫a con el reporte HTML."""
    outcome = yield
    report = outcome.get_result()
    
    # Evaluamos el test en la fase de llamada (cuando se ejecuta el cuerpo del test)
    if report.when == "call":
        # Si el test fall√≥ y el driver est√° disponible en el test, tomamos captura
        if report.failed and hasattr(item, "_driver"):
            driver_instance = item._driver
            os.makedirs("reports", exist_ok=True)
            
            # Nombre √∫nico para la captura basado en el nombre del test
            nombre_limpio = item.name.replace("[", "_").replace("]", "_").replace("-", "_")
            screenshot_path = f"reports/fallback_{nombre_limpio}.png"
            
            try:
                driver_instance.save_screenshot(screenshot_path)
                logger.error(f"Test UI fallido. Captura guardada en: {screenshot_path}")
                
                # C√≥digo HTML para incrustar la imagen directo en el reporte autocontenido
                html_extra = (
                    f'<div><img src="data:image/png;base64,{driver_instance.get_screenshot_as_base64()}" '
                    f'alt="screenshot" style="width:600px;height:auto;" '
                    f'class="screenshot_img"/></div>'
                )
                
                # Agregamos el fragmento de HTML al reporte de pytest-html
                extras = getattr(report, "extras", [])
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    extras.append(pytest_html.extras.html(html_extra))
                    report.extras = extras
            except Exception as e:
                logger.error(f"No se pudo tomar la captura de pantalla: {e}")

# -------------------------------------------------------------------------
# FIXTURE PARA LOGUEAR AL USUARIO POR DEFECTO (UI)
# -------------------------------------------------------------------------
@pytest.fixture(scope="function")
def usuario_logueado(driver):
    """
    Fixture que automatiza el inicio de sesi®Æn previo en SauceDemo
    para los tests que requieren el carrito de compras.
    """
    logger.info("Ejecutando fixture 'usuario_logueado': Iniciando sesi®Æn en SauceDemo")

    # Navegamos a la p®¢gina
    driver.get("https://www.saucedemo.com/")
    
    # Metemos las credenciales est®¢ndar
    username_field = driver.find_element("id", "user-name")
    if hasattr(username_field, "send_with_delay"):
        username_field.send_with_delay("standard_user")
    else:
        username_field.send_keys("standard_user")
        
    driver.find_element("id", "password").send_keys("secret_sauce")
    driver.find_element("id", "login-button").click()

    # Importaci®Æn e instanciaci®Æn alineadas
    from pages.inventory_page import InventoryPage
    inventory_page = InventoryPage(driver)
    
    logger.info("Sesi®Æn iniciada con ®¶xito. Cediendo el control al test.")
    yield driver, inventory_page

# -------------------------------------------------------------------------
# PERSONALIZACI√ìN DE METADATA Y T√çTULO DEL REPORTE HTML
# -------------------------------------------------------------------------
def pytest_html_report_title(report):
    """Configura el t√≠tulo del reporte HTML de forma din√°mica."""
    report.title = "Reporte de Ejecuci√≥n Clase 14-BDD"

@pytest.hookimpl(tryfirst=True)
def pytest_metadata(metadata):
    """Modifica la tabla de metadata del reporte para remover ruido y sumar tus datos."""
    # Sumamos tus datos corporativos
    metadata["Autor"] = "QA Lead Dani"
    metadata["Proyecto"] = "Demo ver login y a√±adir al carrito escritos en Gherkin"
    metadata["Ambiente"] = "QA / Laboratorio"
    
    # Opcional: Remover datos del entorno local que no quieras exponer al cliente
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Packages", None)
    metadata.pop("Plugins", None)