# Python Practical Training

Hands-on Python training project — building practical skills for automation, data processing, and QA through a structured curriculum.

## Progress

- [x] Stage 0 — Environment setup, pytest basics
- [x] Stage 1 — Imports, exceptions, pathlib
- [x] Stage 2 — Text files, CSV, JSON
- [x] Stage 3 — Excel reports (pandas, openpyxl)
- [x] Stage 4 — REST APIs (requests)
- [x] Stage 5 — Web scraping (BeautifulSoup)
- [x] Stage 5.5 — Git & GitHub workflow
- [x] Stage 6 — Advanced pytest
- [x] Stage 6.5 — SQL & databases
- [x] Stage 7 — API testing
- [ ] Stage 8 — Selenium
- [ ] Stage 9 — Portfolio

## Projects

- **Weather pipeline** (`src/weather_api.py`) — fetches data from the Open-Meteo
  API, parses it, and exports to CSV/JSON. Fully tested with mocked HTTP calls.
- **Web scraper** (`src/scraper.py`) — scrapes multi-page weather data with 
  robots.txt checking, custom User-Agent, and rate limiting. Handles dirty 
  real-world data (mixed decimal separators, empty cells, whitespace).
- **Sales report cleaner** (`src/sales_cleaner_html.py`) — extracts and cleans 
  sales data from HTML tables.
- **Validator module** (`src/validator.py`) — input validation (email, price, 
  env-based config) with 100% test coverage.
- **Weather DB pipeline** (`src/weather_report.py`, `src/db_pogoda.py`) — stores 
  scraped weather data in PostgreSQL via psycopg2 (parameterized inserts), 
  reads it back into pandas through SQLAlchemy, and generates an Excel 
  report with average temperature per city.
- **API Testing Suite** (`tests/test_jsonplaceholder.py`, `src/api.py`,
  `tests/test_api.py`) — a QA-style test suite covering both sides of API
  testing: contract tests against a live public API (JSONPlaceholder) checking 
  status codes, response structure, field types, and error paths (404); plus 
  a custom FastAPI app (Pydantic models, path/body validation) with end-to-end 
  tests via TestClient, including negative tests for 422 validation errors.

## Testing

The test suite uses advanced pytest features:

- **Fixtures & conftest.py** — shared test data across test files
- **Parametrization** — single tests covering multiple input cases
- **pytest.raises / pytest.approx** — exception and float testing
- **monkeypatch** — environment variable testing
- **unittest.mock** — mocked HTTP calls (no live requests in tests)
- **pytest-cov** — code coverage measurement

Coverage: `validator.py` 100%, `scraper.py` 87% (excluding CLI entry point).

Run tests:

pytest --cov=src --cov-report=term-missing

## Tech stack

Python 3.13, pytest, pytest-cov, requests, BeautifulSoup4, pandas, openpyxl, 
PostgreSQL, SQLAlchemy, FastAPI, Pydantic