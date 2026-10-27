import pytest

from utils.validation import normalize_phone, parse_guests, validate_name


@pytest.mark.parametrize(("value", "expected"), [("1", 1), ("20", 20), (" 3 ", 3)])
def test_parse_guests_accepts_valid_counts(value, expected):
    assert parse_guests(value) == expected


@pytest.mark.parametrize("value", ["", "0", "21", "1.5", "-1", "два", "２"])
def test_parse_guests_rejects_invalid_counts(value):
    assert parse_guests(value) is None


@pytest.mark.parametrize(
    ("value", "expected"),
    [("Иван Иванов", "Иван Иванов"), ("  Анна   Петрова ", "Анна Петрова"),
     ("Jean-Luc O’Neil", "Jean-Luc O’Neil")],
)
def test_validate_name_normalizes_valid_names(value, expected):
    assert validate_name(value) == expected


@pytest.mark.parametrize(
    "value", ["", "A", "Иван", "12345", "Иван2", "Имя!", "x" * 101]
)
def test_validate_name_rejects_invalid_names(value):
    assert validate_name(value) is None


@pytest.mark.parametrize(
    ("value", "expected"),
    [("+7 924 123-45-67", "+79241234567"), ("8 (924) 123-45-67", "+79241234567"),
     ("9241234567", "+79241234567"), ("+1 202 555 0100", "+12025550100")],
)
def test_normalize_phone_accepts_and_normalizes_numbers(value, expected):
    assert normalize_phone(value) == expected


@pytest.mark.parametrize("value", ["", "123", "+7abc1234567", "++79241234567", "0" * 10])
def test_normalize_phone_rejects_invalid_numbers(value):
    assert normalize_phone(value) is None


