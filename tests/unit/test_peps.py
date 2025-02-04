"""Tests for the class that holds and manages PEPs."""

##############################################################################
# Python imports.
from typing import Final, get_args

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from peplum.app.data import (
    Containing,
    PEPs,
    WithAuthor,
    WithPythonVersion,
    WithStatus,
    WithType,
)
from peplum.app.data.pep import PEP, PEPStatus, PEPType
from peplum.app.data.peps import Filter

##############################################################################
SAMPLE_PEPS: Final[tuple[PEP, ...]] = (
    PEP.from_api(
        {
            "number": 1,
            "title": "PEP Purpose and Guidelines",
            "authors": "Author 1, Author 2, Author 3",
            "author_names": [
                "Author 1",
                "Author 2",
                "Author 3",
            ],
            "discussions_to": None,
            "status": "Active",
            "type": "Process",
            "topic": "",
            "created": "13-Jun-2000",
            "python_version": "3.7, 3.8",
            "post_history": "21-Mar-2001, 29-Jul-2002, 03-May-2003, 05-May-2012, 07-Apr-2013",
            "resolution": None,
            "requires": None,
            "replaces": None,
            "superseded_by": None,
            "url": "https://peps.python.org/pep-0001/",
        }
    ),
    PEP.from_api(
        {
            "number": 458,
            "title": "Secure PyPI downloads with signed repository metadata",
            "authors": "Author 1",
            "author_names": ["Author 1"],
            "discussions_to": "https://discuss.python.org/t/pep-458-secure-pypi-downloads-with-package-signing/2648",
            "status": "Accepted",
            "type": "Standards Track",
            "topic": "packaging",
            "created": "27-Sep-2013",
            "python_version": None,
            "post_history": "06-Jan-2019, 13-Nov-2019",
            "resolution": "https://discuss.python.org/t/pep-458-secure-pypi-downloads-with-package-signing/2648/115",
            "requires": None,
            "replaces": None,
            "superseded_by": None,
            "url": "https://peps.python.org/pep-0458/",
        }
    ),
    PEP.from_api(
        {
            "number": 467,
            "title": "Minor API improvements for binary sequences",
            "authors": "Author 1, Jr.",
            "author_names": ["Author 1, Jr."],
            "discussions_to": "https://discuss.python.org/t/42001",
            "status": "Draft",
            "type": "Informational",
            "topic": "",
            "created": "30-Mar-2014",
            "python_version": "3.13",
            "post_history": "30-Mar-2014, 15-Aug-2014, 16-Aug-2014, 07-Jun-2016, 01-Sep-2016, 13-Apr-2021, 03-Nov-2021, 27-Dec-2023",
            "resolution": None,
            "requires": None,
            "replaces": None,
            "superseded_by": None,
            "url": "https://peps.python.org/pep-0467/",
        }
    ),
    PEP.from_api(
        {
            "number": 639,
            "title": "Improving License Clarity with Better Package Metadata",
            "authors": "Author 1, Author 1, Jr.",
            "author_names": ["Author 1", "Author 1, Jr."],
            "discussions_to": "https://discuss.python.org/t/53020",
            "status": "Provisional",
            "type": "Process",
            "topic": "packaging",
            "created": "15-Aug-2019",
            "python_version": None,
            "post_history": "`15-Aug-2019 <https://discuss.python.org/t/2154>`__, `17-Dec-2021 <https://discuss.python.org/t/12622>`__, `10-May-2024 <https://discuss.python.org/t/53020>`__,",
            "resolution": "https://discuss.python.org/t/53020/106",
            "requires": None,
            "replaces": None,
            "superseded_by": None,
            "url": "https://peps.python.org/pep-0639/",
        }
    ),
    PEP.from_api(
        {
            "number": 213,
            "title": "Attribute Access Handlers",
            "authors": "Author 1, Jr., Author 1",
            "author_names": ["Author 1, Jr.", "Author 1"],
            "discussions_to": None,
            "status": "Deferred",
            "type": "Standards Track",
            "topic": "",
            "created": "21-Jul-2000",
            "python_version": "2.1",
            "post_history": None,
            "resolution": None,
            "requires": None,
            "replaces": None,
            "superseded_by": None,
            "url": "https://peps.python.org/pep-0213/",
        }
    ),
    PEP.from_api(
        {
            "number": 204,
            "title": "Range Literals",
            "authors": "Author 2",
            "author_names": ["Author 2"],
            "discussions_to": None,
            "status": "Rejected",
            "type": "Informational",
            "topic": "",
            "created": "14-Jul-2000",
            "python_version": "2.0",
            "post_history": None,
            "resolution": None,
            "requires": None,
            "replaces": None,
            "superseded_by": None,
            "url": "https://peps.python.org/pep-0204/",
        }
    ),
    PEP.from_api(
        {
            "number": 3,
            "title": "Guidelines for Handling Bug Reports",
            "authors": "Author 1",
            "author_names": ["Author 1"],
            "discussions_to": None,
            "status": "Withdrawn",
            "type": "Process",
            "topic": "",
            "created": "25-Sep-2000",
            "python_version": None,
            "post_history": None,
            "resolution": None,
            "requires": None,
            "replaces": None,
            "superseded_by": None,
            "url": "https://peps.python.org/pep-0003/",
        }
    ),
    PEP.from_api(
        {
            "number": 100,
            "title": "Python Unicode Integration",
            "authors": "Author 1",
            "author_names": ["Author 1"],
            "discussions_to": None,
            "status": "Final",
            "type": "Standards Track",
            "topic": "",
            "created": "10-Mar-2000",
            "python_version": "2.0",
            "post_history": None,
            "resolution": None,
            "requires": None,
            "replaces": None,
            "superseded_by": None,
            "url": "https://peps.python.org/pep-0100/",
        }
    ),
    PEP.from_api(
        {
            "number": 5,
            "title": "Guidelines for Language Evolution",
            "authors": "Author 3",
            "author_names": ["Author 3"],
            "discussions_to": None,
            "status": "Superseded",
            "type": "Informational",
            "topic": "",
            "created": "26-Oct-2000",
            "python_version": None,
            "post_history": None,
            "resolution": None,
            "requires": None,
            "replaces": None,
            "superseded_by": "387",
            "url": "https://peps.python.org/pep-0005/",
        }
    ),
)
"""Some sample PEP data to work off."""


##############################################################################
def test_no_peps() -> None:
    """An empty PEPs object sound have no length."""
    assert len(PEPs()) == 0


##############################################################################
def test_has_peps() -> None:
    """A non-empty PEPs object should report the correct length."""
    assert len(PEPs(SAMPLE_PEPS)) == len(SAMPLE_PEPS)


##############################################################################
def test_status_counts() -> None:
    """We should be able to count the statuses."""
    assert {(status.status, status.count) for status in PEPs(SAMPLE_PEPS).statuses} == {
        (status, 1) for status in get_args(PEPStatus)
    }


##############################################################################
def test_type_counts() -> None:
    """We should be able to count the types."""
    assert {
        (pep_type.type, pep_type.count) for pep_type in PEPs(SAMPLE_PEPS).types
    } == {(pep_type, 3) for pep_type in get_args(PEPType)}


##############################################################################
def test_python_version_counts() -> None:
    """We should be able to count the Python versions."""
    assert {
        (version.version, version.count)
        for version in PEPs(SAMPLE_PEPS).python_versions
    } == {
        ("", 4),
        ("2.0", 2),
        ("2.1", 1),
        ("3.7", 1),
        ("3.8", 1),
        ("3.13", 1),
    }


##############################################################################
def test_author_counts() -> None:
    """We should be able to count the authors."""
    assert {(author.author, author.count) for author in PEPs(SAMPLE_PEPS).authors} == {
        ("Author 1", 6),
        ("Author 1, Jr.", 3),
        ("Author 2", 2),
        ("Author 3", 2),
    }


##############################################################################
@mark.parametrize(
    "pep_filter, expected",
    (
        (Containing("Unicode"), 1),
        (Containing("unicode"), 1),
        (Containing("UNICODE"), 1),
        (Containing("UNICOD"), 1),
        (Containing("NiCOd"), 1),
        (Containing("author 1"), 7),
        (Containing("JR"), 3),
        (Containing("STANDARDS TRACK"), 3),
        (Containing("https://peps.python.org/pep-0467/"), 1),
        (WithAuthor("Author 1, Jr."), 3),
        (WithAuthor("Author 1, Jr"), 0),
        (WithAuthor("author 1"), 6),
        (WithAuthor("AUTHOR 1, JR."), 3),
        (WithAuthor("JR"), 0),
        (WithPythonVersion("3.13"), 1),
        (WithPythonVersion(""), 4),
        (WithStatus("Accepted"), 1),
        (WithType("Standards Track"), 3),
    ),
)
def test_filter(pep_filter: Filter, expected: int) -> None:
    """Test that we can filter a collection of PEPs."""
    assert len(PEPs(SAMPLE_PEPS) & pep_filter) == expected


### test_peps.py ends here
