import os
import logging
from datetime import datetime
from selenium import webdriver

logger = logging.getLogger(__name__)

def before_scenario(context, scenario):
    """Configura un WebDriver limpio antes de CADA escenario, sin alertas de seguridad."""
    logger.info(f"--- INICIANDO ESCENARIO BDD: {scenario.name} ---")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless") # Descomentar para CI/CD si corre en GitHub Actions
    
    # 🚀 CONFIGURACIÓN CLAVE: Desactiva el pop-up de contraseñas vulneradas (Brecha de seguridad)
    prefs = {
        "profile.password_manager_leak_detection": False,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(5)

def after_step(context, step):
    """Captura screenshot automático únicamente si el step actual falla."""
    if step.status == "failed":
        folder_screens = os.path.join("reports", "screens")
        os.makedirs(folder_screens, exist_ok=True)
        
        nombre_limpio = step.name.replace(" ", "_").replace('"', "")
        timestamp = datetime.now().strftime("%H%M%S")
        screenshot_path = os.path.join(folder_screens, f"FAIL_{nombre_limpio}_{timestamp}.png")
        
        try:
            context.driver.save_screenshot(screenshot_path)
            logger.error(f"[BDD FALLO] Step '{step.name}' falló. Evidencia visual guardada en: {screenshot_path}")
        except Exception as e:
            logger.error(f"No se pudo tomar la captura en el fallo de Behave: {e}")

def after_scenario(context, scenario):
    """Cierra el WebDriver de forma segura al finalizar CADA escenario."""
    logger.info(f"--- FINALIZANDO ESCENARIO BDD: {scenario.name} ---")
    if hasattr(context, "driver") and context.driver is not None:
        context.driver.quit()