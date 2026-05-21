def parse_number(value: object) -> float | None:
    """
    Konwertuje value na float. Bezpiecznie obsługuje błędne dane.

    Args:
        value: Dowolna wartość do konwersji.

    Returns:
        float jeśli konwersja się powiodła, None w przeciwnym razie.

    Examples:
        >>> parse_number("3.14")
        3.14
        >>> parse_number("abc")
        >>> parse_number(None)
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def is_positive(value: float) -> bool:
    """
    Sprawdza czy liczba jest dodatnia (większa od zera).

    Args:
        value: Liczba do sprawdzenia.

    Returns:
        True jeśli value > 0, False w przeciwnym razie.

    Examples:
        >>> is_positive(5)
        True
        >>> is_positive(-3)
        False
        >>> is_positive(0)
        False
    """
    return value > 0