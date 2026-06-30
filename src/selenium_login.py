from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_intro import build_chrome_options


def login_to_the_internet(username: str, password: str) -> None:
    """
    Loguje się na stronie testowej podanymi danymi i drukuje komunikat wyniku.

    Args:
        username: login użytkownika do zalogowania.
        password: hasło użytkownika do zalogowania

    Returns:
        None
    """
    driver = webdriver.Chrome(service=Service(),
                              options=build_chrome_options(headless=False))
    try:
        driver.get("https://the-internet.herokuapp.com/login")
        username_pole = driver.find_element(By.ID, "username")
        username_pole.send_keys(username)
        password_pole = driver.find_element(By.ID, "password")
        password_pole.send_keys(password)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']"))).click()
        element = wait.until(
            EC.visibility_of_element_located((By.ID, "flash")))
        print(element.text)
        screenshot_path = Path(
            __file__).parent.parent / "data" / "login_result.png"
        driver.save_screenshot(str(screenshot_path))
    finally:
        driver.quit()


def handle_js_alert() -> None:
    """
    Obsługuje alerty JS i drukuje wynik komunikatu.

    Args:
        Brak.

    Returns:
        None
    """
    driver = webdriver.Chrome(service=Service(),
                              options=build_chrome_options(headless=False))
    try:
        driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        wait = WebDriverWait(driver, 10)
        alert_button = "button[onclick='jsAlert()']"
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, alert_button))).click()
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(alert.text)
        alert.accept()
        result = wait.until(EC.visibility_of_element_located((By.ID,
                                                              "result")))
        print(result.text)
    finally:
        driver.quit()


if __name__ == "__main__":
    login_to_the_internet("tomsmith", "SuperSecretPassword!")