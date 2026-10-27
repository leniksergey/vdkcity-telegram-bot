"""Validation helpers for booking form input."""

import re

MIN_GUESTS = 1
MAX_GUESTS = 20
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 100

_PHONE_SEPARATORS = re.compile(r"[\s().-]")


def parse_guests(value: str) -> int | None:
    """Return a valid guest count, or None for malformed/out-of-range input."""
    value = value.strip()
    if not value.isascii() or not value.isdecimal():
        return None
    guests = int(value)
    return guests if MIN_GUESTS <= guests <= MAX_GUESTS else None


def validate_name(value: str) -> str | None:
    """Normalize a person's name, returning None when it is not plausible."""
    name = " ".join(value.split())
    if not MIN_NAME_LENGTH <= len(name) <= MAX_NAME_LENGTH:
        return None
    if len(name.split()) < 2:
        return None
    if not any(char.isalpha() for char in name):
        return None
    if any(not (char.isalpha() or char in " -'’") for char in name):
        return None
    return name


def normalize_phone(value: str) -> str | None:
    """Validate a phone number and normalize Russian numbers to +7 format."""
    phone = _PHONE_SEPARATORS.sub("", value.strip())
    if phone.startswith("00"):
        phone = "+" + phone[2:]
    if phone.count("+") > 1 or ("+" in phone and not phone.startswith("+")):
        return None
    digits = phone[1:] if phone.startswith("+") else phone
    if not digits.isascii() or not digits.isdecimal() or not 10 <= len(digits) <= 15:
        return None
    if digits.startswith("8") and len(digits) == 11:
        digits = "7" + digits[1:]
    elif len(digits) == 10:
        digits = "7" + digits
    if digits.startswith("0"):
        return None
    return "+" + digits
