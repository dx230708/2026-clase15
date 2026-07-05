import os
import logging
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# -------------------------------------------------------------------------
# CONFIGURACIÓN DE LOGGING UNIFICADO (Criterio 3)
# -------------------------------------------------------------------------
# Nos aseguramos de que exista la carpeta de logs
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)",
    handlers=[
        logging.FileHandler("logs/suite.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()  # Muestra también los logs en la consola
    ]
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------
# FIXTURE DEL WEBDRIVER (INTEGRADO CON LOGS)
# -------------------------------------------------------------------------
@pytest.fixture(scope="function")
def driver(request):
    logger.info(f"Iniciando WebDriver para el test: {request.node.name}")
    
    # Configuración limpia de Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless") # Descomentar para GitHub Actions
    
    driver = webdriver.Chrome(options=options)
    
    # Adjuntamos el driver al nodo del test para que el hook de reporte pueda acceder a él si falla
    request.node._driver = driver
    
    yield driver
    
    logger.info(f"Cerrando WebDriver para el test: {request.node.name}")
    driver.quit()

# -------------------------------------------------------------------------
# HOOKS DE REPORTE HTML Y CAPTURA EN CASO DE FALLO (Criterio 2)
# -------------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Detecta el resultado de cada fase del test e interactúa con el reporte HTML."""
    outcome = yield
    report = outcome.get_result()
    
    # Evaluamos el test en la fase de llamada (cuando se ejecuta el cuerpo del test)
    if report.when == "call":
        # Si el test falló y el driver está disponible en el test, tomamos captura
        if report.failed and hasattr(item, "_driver"):
            driver_instance = item._driver
            os.makedirs("reports", exist_ok=True)
            
            # Nombre único para la captura basado en el nombre del test
            nombre_limpio = item.name.replace("[", "_").replace("]", "_").replace("-", "_")
            screenshot_path = f"reports/fallback_{nombre_limpio}.png"
            
            try:
                driver_instance.save_screenshot(screenshot_path)
                logger.error(f"Test UI fallido. Captura guardada en: {screenshot_path}")
                
                # Código HTML para incrustar la imagen directo en el reporte autocontenido
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
    Fixture que automatiza el inicio de sesión previo en SauceDemo
    para los tests que requieren el carrito de compras.
    """
    logger.info("Ejecutando fixture 'usuario_logueado': Iniciando sesión en SauceDemo")
    
    # Navegamos a la página
    driver.get("https://www.saucedemo.com/")
    
    # Metemos las credenciales estándar (podés ajustarlo si usás variables o config)
    driver.find_element("id", "user-name").send_with_delay("standard_user") if hasattr(driver.find_element("id", "user-name"), "send_with_delay") else driver.find_element("id", "user-name").send_keys("standard_user")
    driver.find_element("id", "password").send_keys("secret_sauce")
    driver.find_element("id", "login-button").click()
    
    logger.info("Sesión iniciada con éxito. Cediendo el control al test.")
    yield driver

# -------------------------------------------------------------------------
# PERSONALIZACIÓN DE METADATA Y TÍTULO DEL REPORTE HTML
# -------------------------------------------------------------------------
def pytest_html_report_title(report):
    """Configura el título del reporte HTML de forma dinámica."""
    report.title = "Reporte de Ejecución Clase 14-BDD"

@pytest.hookimpl(tryfirst=True)
def pytest_metadata(metadata):
    """Modifica la tabla de metadata del reporte para remover ruido y sumar tus datos."""
    # Sumamos tus datos corporativos
    metadata["Autor"] = "QA Lead Dani"
    metadata["Proyecto"] = "Demo ver login y añadir al carrito escritos en Gherkin"
    metadata["Ambiente"] = "QA / Laboratorio"
    
    # Opcional: Remover datos del entorno local que no quieras exponer al cliente
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Packages", None)
    metadata.pop("Plugins", None)