"""Tests relating to the parsing of dates."""

##############################################################################
# Python imports.
from datetime import date
from itertools import chain

##############################################################################
# Pytest imports.
from pytest import mark, raises

##############################################################################
# Local imports.
from peplum.app.data.pep import parse_date


##############################################################################
@mark.parametrize(
    "month_name, month_number",
    chain(
        *(
            (
                (name, number),
                (name.upper(), number),
                (name.lower(), number),
                (name.swapcase(), number),
            )
            for name, number in (
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
        )
    ),
)
def test_parse_pep_date(month_name: str, month_number: int) -> None:
    """We should be able to parse dates as found in the PEP index."""
    assert parse_date(f"01-{month_name}-2025") == date(2025, month_number, 1)


##############################################################################
@mark.parametrize(
    "dodgy_date",
    (
        "32-Jan-2025",
        "29-Feb-2025",
        "32-Mar-2025",
        "31-Apr-2025",
        "32-May-2025",
        "31-Jun-2025",
        "32-Jul-2025",
        "32-Aug-2025",
        "31-Sep-2025",
        "32-Oct-2025",
        "31-Nov-2025",
        "32-Dec-2025",
        "01-non-2025",
        "111-Jan-2025",
        "1-Jan-22025",
        "01-Jan-22025",
        "0001-Jan-22025",
        "01/Jan/2025",
        "",
    ),
)
def test_parse_dodgy_date(dodgy_date: str) -> None:
    """We should detect dodgy dates when parsing them."""
    with raises(ValueError):
        _ = parse_date(dodgy_date)


### test_pep_dates.py ends here
