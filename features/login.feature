@ui
Feature: Autenticación de Usuarios en SauceDemo
  Como usuario de la plataforma
  Quiero ingresar mis credenciales
  Para poder acceder al catálogo de productos

  Background: Abrir la pantalla de login
    Given el usuario se encuentra en la página de inicio de sesión

  @smoke
  Scenario: Inicio de sesión exitoso con credenciales válidas
    When el usuario ingresa el usuario "standard_user" y la clave "secret_sauce"
    And hace clic en el botón de ingresar
    Then es redirigido a la página de inventario "inventory.html"

  Scenario Outline: Intento de inicio de sesión fallido
    When el usuario ingresa el usuario "<usuario>" y la clave "<clave>"
    And hace clic en el botón de ingresar
    Then se muestra un mensaje de error que contiene "<mensaje_error>"

    Examples: Casos de Error
      | usuario         | clave          | mensaje_error                                              |
      | invalid_user    | secret_sauce   | Username and password do not match any user in this service|
      | locked_out_user | secret_sauce   | Sorry, this user has been locked out.                      |
      |                 | secret_sauce   | Username is required                                       |