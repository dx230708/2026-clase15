import logging
from behave import given, when, then
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)

@given("el usuario se encuentra en la página de inicio de sesión")
def step_open_login_page(context):
    logger.info("Abriendo página de login de SauceDemo")
    context.login_page = LoginPage(context.driver)
    context.driver.get("https://www.saucedemo.com/")

@when('el usuario ingresa el usuario "{usuario}" y la clave "{clave}"')
def step_input_credentials(context, usuario, clave):
    logger.info(f"Ingresando credenciales - Usuario: '{usuario}'")
    # Usamos los métodos de tu Page Object real
    context.login_page.username_input.send_keys(usuario) if hasattr(context.login_page, 'username_input') else context.driver.find_element("id", "user-name").send_keys(usuario)
    context.driver.find_element("id", "password").send_keys(clave)

@when("hace clic en el botón de ingresar")
def step_click_login(context):
    logger.info("Haciendo clic en botón de Login")
    context.driver.find_element("id", "login-button").click()

@then('es redirigido a la página de inventario "{pagina_esperada}"')
def step_validate_redirect(context, pagina_esperada):
    logger.info(f"Validando redirección a {pagina_esperada}")
    url_actual = context.driver.current_url
    assert pagina_esperada in url_actual, f"Redirección fallida. URL actual: {url_actual}"

@then('se muestra un mensaje de error que contiene "{mensaje_error}"')
def step_validate_error_message(context, mensaje_error):
    logger.info(f"Validando presencia del mensaje de error: '{mensaje_error}'")
    error_element = context.driver.find_element("xpath", "//h3[@data-test='error']")
    texto_error = error_element.text
    assert mensaje_error in texto_error, f"Se esperaba '{mensaje_error}' pero se leyó '{texto_error}'"