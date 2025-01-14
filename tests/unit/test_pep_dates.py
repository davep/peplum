"""Tests relating to the parsing of dates."""

##############################################################################
# Python imports.
from datetime import date
from locale import LC_TIME, getlocale, setlocale

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from peplum.peps.pep import parse_date

##############################################################################
MONTHS = (
    ("Jan", 1),
    ("Feb", 2),
    ("Mar", 3),
    ("Apr", 4),
    ("May", 5),
    ("Jun", 6),
    ("Jul", 7),
    ("Aug", 8),
    ("Sep", 9),
    ("Oct", 10),
    ("Nov", 11),
    ("Dec", 12),
)
"""Month names and their numbers."""


##############################################################################
@mark.parametrize("month_name, month_number", MONTHS)
def test_parse_pep_date(month_name: str, month_number: int) -> None:
    """We should be able to parse dates as found in the PEP index."""
    assert parse_date(f"01-{month_name}-2025") == date(2025, month_number, 1)


##############################################################################
@mark.parametrize("month_name, month_number", MONTHS)
def test_parse_pep_date_outwith_english(month_name: str, month_number: int) -> None:
    """We should be able to parse dates as found in the PEP index no matter our locale."""
    our_locale = getlocale(LC_TIME)
    try:
        setlocale(LC_TIME, "fr_FR")
        assert parse_date(f"01-{month_name}-2025") == date(2025, month_number, 1)
    finally:
        setlocale(LC_TIME, our_locale)


### test_pep_dates.py ends here
