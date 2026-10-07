"""
Funciones auxiliares para las pruebas de saucedemo.com.
Incluye esperas explícitas, login reutilizable y capturas de pantalla.
"""
import logging
import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

# ---------- Datos de prueba ----------
URL_BASE = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
CLAVE_VALIDA = "secret_sauce"
TIEMPO_ESPERA = 10  # segundos máximos de espera explícita
CARPETA_CAPTURAS = os.path.join("reports", "capturas")


def esperar_elemento_visible(driver, localizador, timeout=TIEMPO_ESPERA):
    """Espera a que un elemento sea visible y lo devuelve.

    localizador: tupla (tipo de búsqueda, valor), por ejemplo (By.ID, "user-name").
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(localizador)
    )


def esperar_url_contiene(driver, texto, timeout=TIEMPO_ESPERA):
    """Espera (explícita) a que la URL actual contenga el texto indicado."""
    return WebDriverWait(driver, timeout).until(EC.url_contains(texto))


def hacer_login(driver, usuario=USUARIO_VALIDO, clave=CLAVE_VALIDA):
    """Abre saucedemo e inicia sesión. Se usa en los tests que necesitan estar logueados."""
    logger.info("Navegando a %s", URL_BASE)
    driver.get(URL_BASE)

    espera = WebDriverWait(driver, TIEMPO_ESPERA)
    campo_usuario = espera.until(EC.visibility_of_element_located((By.ID, "user-name")))
    campo_clave = espera.until(EC.visibility_of_element_located((By.ID, "password")))
    boton_login = espera.until(EC.element_to_be_clickable((By.ID, "login-button")))

    campo_usuario.send_keys(usuario)
    campo_clave.send_keys(clave)
    boton_login.click()

    esperar_url_contiene(driver, "/inventory.html")
    # Espera explícita a que los productos estén visibles antes de seguir
    esperar_elemento_visible(driver, (By.CLASS_NAME, "inventory_item"))
    logger.info("Login realizado con el usuario '%s'", usuario)


def capturar_pantalla(driver, nombre_test):
    """Guarda una captura en reports/capturas/ con el nombre del test y la hora."""
    os.makedirs(CARPETA_CAPTURAS, exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = os.path.join(CARPETA_CAPTURAS, f"{nombre_test}_{marca_tiempo}.png")
    driver.save_screenshot(ruta)
    logger.error("Test fallido. Captura guardada en %s", ruta)