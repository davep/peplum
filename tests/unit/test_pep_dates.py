"""Tests relating to the parsing of dates."""

##############################################################################
# Python imports.
from datetime import date

##############################################################################
# Pytest imports.
from pytest import mark, raises

##############################################################################
# Local imports.
from peplum.peps.pep import parse_date


##############################################################################
@mark.parametrize(
    "month_name, month_number",
    (
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
    ),
)
def test_parse_pep_date(month_name: str, month_number: int) -> None:
    """We should be able to parse dates as found in the PEP index."""
    assert parse_date(f"01-{month_name}-2025") == date(2025, month_number, 1)


##############################################################################
@mark.parametrize(
    "dodgy_date",
    (
        "01-non-2025",
        "111-Jan-2025",
        "1-Jan-22025",
        "01-Jan-22025",
        "0001-Jan-22025",
        "",
    ),
)
def test_parse_dodgy_date(dodgy_date: str) -> None:
    """We should detect dodgy dates when parsing them."""
    with raises(ValueError):
        _ = parse_date(dodgy_date)


### test_pep_dates.py ends here
