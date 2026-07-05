import logging
from behave import given, when, then
from pages.inventory_page import InventoryPage

logger = logging.getLogger(__name__)

@given("el usuario se encuentra logueado con credenciales estándar")
def step_logged_in_background(context):
    logger.info("Ejecutando Background: Logueando standard_user")
    context.driver.get("https://www.saucedemo.com/")
    context.driver.find_element("id", "user-name").send_keys("standard_user")
    context.driver.find_element("id", "password").send_keys("secret_sauce")
    context.driver.find_element("id", "login-button").click()
    context.inventory_page = InventoryPage(context.driver)

@when('el usuario agrega el producto "{nombre_producto}" usando su localizador por defecto')
def step_add_product_cart(context, nombre_producto):
    logger.info(f"Agregando producto al carrito: {nombre_producto}")
    # Reutilizás dinámicamente tu lógica POM basada en XPATH o JSON de productos
    # Mapeo rápido para cumplir el requerimiento de Sauce Labs Backpack
    if "Backpack" in nombre_producto:
        xpath = "//button[@data-test='add-to-cart-sauce-labs-backpack']"
    else:
        xpath = "//button[@data-test='add-to-cart-sauce-labs-bike-light']"
        
    context.inventory_page.agregar_producto_por_xpath(xpath)

@then('el contador del icono del carrito debe mostrar "{cantidad_esperada}"')
def step_validate_cart_badge(context, cantidad_esperada):
    logger.info(f"Validando contador del carrito. Esperado: {cantidad_esperada}")
    badge_element = context.driver.find_element("class name", "shopping_cart_badge")
    assert badge_element.text == cantidad_esperada, f"Contador incorrecto. Esperado {cantidad_esperada}, obtenido {badge_element.text}"