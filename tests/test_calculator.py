# tests/test_calculator.py

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator import divide, safe_sqrt, calculate
from utils import parse_number


# --- parse_number ---

def test_parse_number_valid_string():
    assert parse_number("3.14") == 3.14

def test_parse_number_integer():
    assert parse_number(10) == 10.0

def test_parse_number_invalid_returns_none():
    assert parse_number("abc") is None

def test_parse_number_none_input_returns_none():
    assert parse_number(None) is None


# --- divide ---

def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_by_zero_returns_none():
    assert divide(5, 0) is None


# --- safe_sqrt ---

def test_sqrt_positive():
    assert safe_sqrt(9) == 3.0

def test_sqrt_negative_returns_none():
    assert safe_sqrt(-1) is None


# --- calculate ---

def test_calculate_add():
    assert calculate("10", "5", "add") == 15.0

def test_calculate_divide_by_zero():
    assert calculate("10", "0", "divide") is None

def test_calculate_invalid_input():
    assert calculate("abc", "5", "add") is None

def test_calculate_zero_as_first_argument():
    assert calculate("0", "5", "add") == 5.0

def test_calculate_unknown_operation_returns_none():
    assert calculate("10", "5", "modulo") is None
