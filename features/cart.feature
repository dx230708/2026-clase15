@ui @regression
Feature: Funcionalidad del Carrito de Compras
  Como usuario autenticado
  Quiero agregar productos al carrito
  Para poder gestionar mi orden de compra

  Background: Sesión iniciada automáticamente
    Given el usuario se encuentra logueado con credenciales estándar

  Scenario: Agregar un producto individual al carrito con éxito
    When el usuario agrega el producto "Sauce Labs Backpack" usando su localizador por defecto
    Then el contador del icono del carrito debe mostrar "1"

  Scenario: Agregar múltiples productos y verificar acumulación
    When el usuario agrega el producto "Sauce Labs Backpack" usando su localizador por defecto
    And el usuario agrega el producto "Sauce Labs Bike Light" usando su localizador por defecto
    Then el contador del icono del carrito debe mostrar "2"