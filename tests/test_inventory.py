"""
Test de navegación y verificación del catálogo de productos.
"""
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from utils.helpers import capturar_pantalla, esperar_elemento_visible, hacer_login

logger = logging.getLogger(__name__)


def test_catalogo_navegacion():
    driver = webdriver.Chrome()

    try:
        hacer_login(driver)

        # 1. Validar el título de la página
        titulo = esperar_elemento_visible(driver, (By.CSS_SELECTOR, "[data-test='title']"))
        assert titulo.text == "Products", f"Título inesperado: {titulo.text}"
        assert driver.title == "Swag Labs", f"Título de pestaña inesperado: {driver.title}"

        # 2. Validar que existan productos visibles
        productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(productos) > 0, "No se encontraron productos en el catálogo"
        logger.info("Productos encontrados: %d", len(productos))

        # 3. Validar elementos: menú y filtro
        menu = esperar_elemento_visible(driver, (By.ID, "react-burger-menu-btn"))
        assert menu.is_displayed(), "No se muestra el botón de menú"

        filtro = esperar_elemento_visible(driver, (By.CLASS_NAME, "product_sort_container"))
        assert filtro.is_displayed(), "No se muestra el filtro de orden"
        assert len(Select(filtro).options) > 0, "El filtro no tiene opciones"

        # 4. Detallar nombre y precio del primer producto
        primer_producto = productos[0]
        nombre = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
        precio = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text
        assert nombre != "", "El primer producto no tiene nombre"
        assert precio.startswith("$"), f"Precio con formato inesperado: {precio}"
        logger.info("Primer producto: %s - %s", nombre, precio)
        print(f"Primer producto: {nombre} - {precio}")

    except Exception:
        capturar_pantalla(driver, "test_catalogo_navegacion")
        raise
    finally:
        driver.quit()