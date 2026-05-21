from pathlib import Path


def save_text(path, content):
    """
    Zapisuje content do pliku pod ścieżką path.
    Tworzy plik jeśli nie istnieje. Nadpisuje jeśli istnieje.
    Zwraca True jeśli zapis się udał, False jeśli nie.

    path: string lub Path
    content: string
    """
    # TODO: użyj with open() w trybie "w" z encoding="utf-8"
    # Obsłuż wyjątek OSError (błąd zapisu, brak uprawnień itp.)
    # Zwróć True lub False
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except OSError:
        return False

def read_text(path):
    """
    Czyta zawartość pliku i zwraca jako string.
    Zwraca None jeśli plik nie istnieje lub błąd odczytu.

    path: string lub Path
    """
    # TODO: użyj with open() w trybie "r" z encoding="utf-8"
    # Obsłuż FileNotFoundError i OSError osobno
    # Zwróć zawartość lub None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except OSError:
        return None


def read_lines(path):
    """
    Czyta plik i zwraca listę linii (bez \n na końcach).
    Pomija puste linie.
    Zwraca None jeśli plik nie istnieje.

    Przykład — plik zawiera:
        "Anna\n\nBart\nCelina\n"
    Wynik:
        ["Anna", "Bart", "Celina"]
    """
    # TODO: wczytaj linie, użyj strip(), pomiń puste
    # Wskazówka: line.strip() != "" to warunek niepustej linii
    try:
        with open(path, 'r', encoding='utf-8') as f:
            result = []
            for line in f:
                stripped = line.strip()
                if stripped:
                    result.append(stripped)
            return result
    except FileNotFoundError:
        return None


def append_line(path, line):
    try:
        # Sprawdź czy plik istnieje i czy kończy się \n
        prefix = ""
        if Path(path).exists():
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if content and not content.endswith("\n"):
                prefix = "\n"

        # Dopisz
        with open(path, 'a', encoding='utf-8') as f:
            f.write(prefix + line + "\n")
        return True
    except OSError:
        return False
