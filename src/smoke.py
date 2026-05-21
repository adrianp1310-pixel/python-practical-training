def add(a, b):
    return a + b


def greet(name):
    return f"Cześć, {name}!"

if __name__ == "__main__":
    import pandas as pd
    from pathlib import Path

    DATA_DIR = Path(__file__).parent.parent / "data" / "monthly"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    months = {
        "january.csv": [
            {"product": "Laptop Dell",     "category": "Elektronika", "quantity": 5,  "unit_price": 3500},
            {"product": "Mysz Logitech",   "category": "Elektronika", "quantity": 20, "unit_price": 89},
            {"product": "Krzesło biurowe", "category": "Meble",       "quantity": 8,  "unit_price": 750},
        ],
        "february.csv": [
            {"product": "Laptop Dell",     "category": "Elektronika", "quantity": 3,  "unit_price": 3500},
            {"product": "Biurko",          "category": "Meble",       "quantity": 4,  "unit_price": 1200},
            {"product": "Klawiatura",      "category": "Elektronika", "quantity": 15, "unit_price": 220},
            {"product": "Lampka LED",      "category": "Oświetlenie", "quantity": 25, "unit_price": 110},
        ],
        "march.csv": [
            {"product": "Monitor LG",      "category": "Elektronika", "quantity": 7,  "unit_price": 1800},
            {"product": "Słuchawki Sony",  "category": "Elektronika", "quantity": 12, "unit_price": 450},
            {"product": "Biurko",          "category": "Meble",       "quantity": 2,  "unit_price": 1200},
        ],
    }

    for filename, data in months.items():
        df = pd.DataFrame(data)
        df.to_csv(DATA_DIR / filename, index=False)
        print(f"Zapisano: {DATA_DIR / filename}")