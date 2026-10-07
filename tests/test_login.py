"""
Test de login
"""
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import capturar_pantalla, esperar_url_contiene

logger = logging.getLogger(__name__)


def test_login_exitoso():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.saucedemo.com/")

        # Esperas explícitas: cada elemento debe estar listo antes de usarlo
        usuario = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))
        boton_login = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))

        usuario.send_keys("standard_user")
        password.send_keys("secret_sauce")
        boton_login.click()

        # Espera explícita a que cargue la página de productos
        esperar_url_contiene(driver, "/inventory.html")
        assert "/inventory.html" in driver.current_url

        # Validación de texto
        logo = driver.find_element(By.CLASS_NAME, "app_logo")
        assert logo.text == "Swag Labs"

        titulo = driver.find_element(By.CSS_SELECTOR, "[data-test='title']")
        assert titulo.text == "Products"
        logger.info("Login exitoso validado")

    except Exception:
        capturar_pantalla(driver, "test_login_exitoso")
        raise
    finally:
        driver.quit()