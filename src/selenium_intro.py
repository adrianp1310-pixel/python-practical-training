from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def build_chrome_options(headless: bool = True) -> Options:
    """
    Buduje skonfigurowany obiekt Options dla Chrome

    Args:
        headless: Jeśli True, Chrome działa bez okna (tryb headless).

    Returns:
         Options: obiekt z ustawionym rozmiarem okna, User-Agent i
         opcjonalnie trybem headless.
    """
    options = Options()
    if headless is True:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    return options


def open_example_page() -> None:
    """
    Otwiera example.com w Chrome i drukuje tytuł strony.

    Args:
        Brak.

    Returns:
        None. Wynik (tytuł) trafia na stdout przez print.
    """
    driver = webdriver.Chrome(service=Service(),
                              options=build_chrome_options(headless=False))
    try:
        driver.get("https://example.com")
        print(driver.title)
    finally:
        driver.quit()


def read_example_content() -> None:
    """
    Czyta kontent ze strony i wyświetla jego elementy.

    Args:
        Brak.

    Returns:
        None
    """
    driver = webdriver.Chrome(service=Service(),
                              options=build_chrome_options(headless=False))
    try:
        driver.get("https://example.com")
        head = driver.find_element(By.TAG_NAME, "h1")
        print(head.text)
        links = driver.find_elements(By.TAG_NAME, "a")
        print(len(links))
        for link in links:
            print(link.get_attribute("href"))
    finally:
        driver.quit()


def read_with_wait() -> None:
    """
    Czyta kontent ze strony i wyświetla jego elementy, czekając aż element
    będzie widoczny

    Args:
        Brak.

    Returns:
        None
    """
    driver = webdriver.Chrome(service=Service(),
                              options=build_chrome_options(headless=False))
    try:
        driver.get("https://example.com")
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.TAG_NAME,
                                                               "h1")))
        print(element.text)
    finally:
        driver.quit()


if __name__ == "__main__":
    open_example_page()
    read_example_content()
    read_with_wait()