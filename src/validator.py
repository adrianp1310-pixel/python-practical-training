import os


def validate_email(email: str) -> str:
    """
    Sprawdza, czy email zawiera dokładne jeden "@" i co najmniej jedną "."
    
    Args:
        email (str): email do sprawdzenia.
        
    Returns:
        str: email stripped
    """
    email = email.strip()
    if email.count("@") != 1 or email.split("@")[1].count(".") < 1:
        raise ValueError("Email niepoprawny")
    return email


def validate_price(raw: str) -> float:
    """
    Konwertuje, string cenowy na float obsługując przecinek i spacje po
    tysiącach

    Args:
        raw (str): Cena jako string do skonwertowania.

    Returns:
        float: Cena po skonwertowaniu.
    """
    raw = raw.replace(" ", "").replace(",", ".")
    try:
        price = float(raw)
    except ValueError:
        raise ValueError(f"Nieprawidłowa cena: {raw}")
    if price <= 0:
        raise ValueError(f"Cena musi być dodatnia: {raw}")
    return price


def load_config() -> dict:
    """
    Czyta zmienne środowiskowe APP_NAME i APP_DEBUG.

    Returns:
        dict: słownik zmiennych środowiskowych.
    """
    app_name = os.environ.get("APP_NAME")
    if app_name is None:
        raise ValueError("APP_NAME nie istnieje")
    app_debug = os.environ.get("APP_DEBUG", "")
    debug = app_debug.lower() in ("true", "1")
    return {"app_name": app_name, "debug": debug}

