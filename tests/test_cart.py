"""
Test de interacción con productos y carrito de compras
"""
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

from utils.helpers import (
    capturar_pantalla, esperar_elemento_visible, esperar_url_contiene, hacer_login,
)

logger = logging.getLogger(__name__)


def test_agregar_producto_al_carrito():
    driver = webdriver.Chrome()

    try:
        hacer_login(driver)

        # 1. Tomar el primer producto y guardar su nombre
        primer_producto = driver.find_elements(By.CLASS_NAME, "inventory_item")[0]
        nombre_esperado = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text

        # 2. Agregarlo al carrito (botón DENTRO del primer producto)
        boton_agregar = primer_producto.find_element(By.CSS_SELECTOR, "button.btn_inventory")
        boton_agregar.click()
        logger.info("Producto agregado: %s", nombre_esperado)

        # 3. Verificar que el contador del carrito muestre 1
        contador = esperar_elemento_visible(driver, (By.CLASS_NAME, "shopping_cart_badge"))
        assert contador.text == "1", f"Contador esperado: 1, obtenido: {contador.text}"

        # 4. Navegar al carrito
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        esperar_url_contiene(driver, "/cart.html")

        # 5. Verificar que el producto aparezca en el carrito
        esperar_elemento_visible(driver, (By.CLASS_NAME, "cart_item"))
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) == 1, f"Se esperaba 1 ítem en el carrito, hay {len(items)}"

        nombre_en_carrito = items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
        assert nombre_en_carrito == nombre_esperado, (
            f"Se esperaba '{nombre_esperado}' pero el carrito contiene '{nombre_en_carrito}'"
        )

    except Exception:
        capturar_pantalla(driver, "test_agregar_producto_al_carrito")
        raise
    finally:
        driver.quit()