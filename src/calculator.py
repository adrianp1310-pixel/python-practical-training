import math

from utils import parse_number

def divide(a: float, b: float) -> float | None:
    """
    Dzieli a przez b. Bezpiecznie obsługuje dzielenie przez zero.

    Args:
        a: Liczba dzielona.
        b: Liczba dzielnik.

    Returns:
        Wynik dzielenia. None jeśli b == 0.

    Examples:
        >>> divide(10, 2)
        5.0
        >>> divide(5, 0)
        >>> divide(-6, 3)
        -2.0
    """
    if b == 0:
        return None
    return a / b


def safe_sqrt(value: float) -> float | None:
    """
    Liczy pierwiastek kwadratowy z value. Bezpiecznie obsługuje liczby ujemne.

    Args:
        value: Liczba pod pierwiastkiem.

    Returns:
        Pierwiastek kwadratowy z value. None jeśli value < 0.

    Examples:
        >>> safe_sqrt(9)
        3.0
        >>> safe_sqrt(2)
        1.4142135623730951
        >>> safe_sqrt(-1)
    """
    try:
        return math.sqrt(value)
    except ValueError:
        return None


def calculate(raw_a: object, raw_b: object, operation: str) -> float | None:
    """
    Wykonuje operacje matematyczne takie jak dodawanie, odejmowanie, mnożenie i dzielenie
    liczby a i b w zależności od podanej operation.

    Args:
        raw_a: Surowa wartość pierwszego argumentu (string lub liczba).
        raw_b: Surowa wartość drugiego argumentu (string lub liczba).
        operation: Nazwa operacji. Dozwolone wartości:
            - "add" — dodawanie
            - "subtract" — odejmowanie
            - "multiply" — mnożenie
            - "divide" — dzielenie

    Returns:
        Wynik operacji matematycznej. None jeśli a lub b is None lub operation jest niepoprawny.

    Examples:
        >>> calculate(10, 20, "add")
        30.0
        >>> calculate("5", "3", "subtract")
        2.0
        >>> calculate("abc", 5, "add")
        >>> calculate(10, 20, "modulo")
    """

    a = parse_number(raw_a)
    if a is None:
        return None
    b = parse_number(raw_b)
    if b is None:
        return None
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return divide(a, b)
    else:
        return None
