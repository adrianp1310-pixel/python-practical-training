import logging
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_intro import build_chrome_options

logger = logging.getLogger(__name__)


def login(driver, username: str, password: str) -> None:
    """
    Loguje się strony tekstowej. Driver dostaje z zewnątrz.

    Args:
        driver: sterownik przeglądarki.
        username: nazwa użytkownika do logowania.
        password: hasło do logowania.

    Returns:
        None
    """
    driver.get("https://the-internet.herokuapp.com/login")
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()
    element = wait.until(EC.visibility_of_element_located((By.ID, "flash")))
    logger.info("Zalogowano na stronie jako %s. Odczyt strony: %s",
                username, element.text)


def logout(driver) -> None:
    """
    Wylogowuje się z /secure i weryfikuje powrót na /login.

    Args:
        driver: sterownik przeglądarki.

    Returns:
        None
    """
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/logout']"))
    ).click()
    element = wait.until(EC.visibility_of_element_located((By.ID, "flash")))
    logger.info("Wylogowano. Odczyt ze strony: %s", element.text)


def run_bot(headless: bool) -> None:
    """
    Uruchamia bota który wykonuje logowanie, zrzut ekranu, wylogowanie. Tworzy
    drivera i obsługuje wyjątki.

    Args:
        headless: tryb okna przeglądarki.

    Returns:
        None
    """
    driver = webdriver.Chrome(service=Service(),
                              options=build_chrome_options(headless=headless))
    try:
        logger.info("Start bota")
        login(driver, "tomsmith", "SuperSecretPassword!")
        screenshot_path = (Path(__file__).parent.parent / "data" /
                           "screenshot.png")
        save_screenshot = driver.save_screenshot(str(screenshot_path))
        if save_screenshot is True:
            logger.info("Pomyślnie zapisano zrzut ekranu.")
        else:
            logger.warning("Błąd zapisu screenshootu")
        logout(driver)
    except TimeoutException:
        logger.error("Timeout podczas scenariusza", exc_info=True)
    finally:
        driver.quit()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    run_bot(headless=True)
