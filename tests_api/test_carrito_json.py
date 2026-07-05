import os
import pytest
from utils.datos import leer_json_productos
from pages.inventory_page import InventoryPage

# Carga de la lista de diccionarios desde productos.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_JSON = os.path.join(BASE_DIR, "datos", "productos.json")
PRODUCTOS = leer_json_productos(RUTA_JSON)

@pytest.mark.web
@pytest.mark.parametrize("producto", PRODUCTOS)
def test_agregar_producto_desde_json(usuario_logueado, producto):
    """
    Test que agrega cada producto del JSON al carrito de manera individual.
    Comprueba la persistencia del contador (badge) con diferentes elementos.
    """
    # 1. Asignamos el driver recibido directamente desde el fixture
    driver = usuario_logueado 
    
    # 2. Instanciamos el Page Object pasándole el driver real
    inventory = InventoryPage(driver)
    
    nombre = producto["nombre"]
    xpath = producto["xpath_add_button"]
    
    # Interacción dinámica basada en el JSON
    inventory.agregar_producto_por_xpath(xpath)
    
    # Validación del incremento
    contador = inventory.obtainer_contador_carrito() if hasattr(inventory, 'obtainer_contador_carrito') else inventory.obtener_contador_carrito()
    assert contador == "1", f"El badge no marcó '1' al añadir el producto: {nombre}"


@pytest.mark.smoke
def test_carrito_smoke(usuario_logueado):
    """
    Test de smoke que verifica funcionalidad básica del carrito de compras.
    Flujo rápido: Añade el primer producto disponible y valida navegación básica.
    """
    driver, inventory = usuario_logueado
    
    # Usamos el primer ítem del JSON cargado para el smoke test rápido
    primer_producto = PRODUCTOS[0]
    
    inventory.agregar_producto_por_xpath(primer_producto["xpath_add_button"])
    
    # Navegación a la interfaz del carrito para confirmar ruta
    inventory.ir_al_carrito()
    assert "/cart.html" in driver.current_url, "Fallo al navegar a la pantalla del carrito de compras."