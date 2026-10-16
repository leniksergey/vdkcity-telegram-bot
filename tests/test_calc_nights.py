from datetime import date

from handlers.booking_handlers.booking_handlers import _calc_nights


def test_calc_nights_simple():
    data = {
        "checkin_obj": date(2026, 1, 1),
        "checkout_obj": date(2026, 1, 5),
    }
    assert _calc_nights(data) == 4


def test_calc_nights_one_night():
    data = {
        "checkin_obj": date(2026, 1, 1),
        "checkout_obj": date(2026, 1, 2),
    }
    assert _calc_nights(data) == 1


def test_calc_nights_missing_dates():
    assert _calc_nights({}) == 0


def test_calc_nights_missing_checkout():
    data = {"checkin_obj": date(2026, 1, 1)}
    assert _calc_nights(data) == 0
