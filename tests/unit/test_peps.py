"""Tests for the class that holds and manages PEPs."""

##############################################################################
# Python imports.
from typing import Final, get_args

##############################################################################
# Local imports.
from peplum.app.data import PEPs, StatusCount, TypeCount
from peplum.peps import PEP, PEPStatus, PEPType

##############################################################################
SAMPLE_PEPS: Final[tuple[PEP, ...]] = (
    PEP.from_json(
        {
            "number": 1,
            "title": "PEP Purpose and Guidelines",
            "authors": "Barry Warsaw, Jeremy Hylton, David Goodger, Alyssa Coghlan",
            "discussions_to": None,
            "status": "Active",
            "type": "Process",
            "topic": "",
            "created": "13-Jun-2000",
            "python_version": None,
            "post_history": "21-Mar-2001, 29-Jul-2002, 03-May-2003, 05-May-2012, 07-Apr-2013",
            "resolution": None,
            "requires": None,
            "replaces": None,
            "superseded_by": None,
            "url": "https://peps.python.org/pep-0001/",
        }
    ),
    PEP.from_json(
        {
            "number": 458,
            "title": "Secure PyPI downloads with signed repository metadata",
            "authors": "Trishank Karthik Kuppusamy, Vladimir Diaz, Marina Moore, Lukas Puehringer, Joshua Lock, Lois Anne DeLong, Justin Cappos",
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
    PEP.from_json(
        {
            "number": 467,
            "title": "Minor API improvements for binary sequences",
            "authors": "Alyssa Coghlan, Ethan Furman",
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
    PEP.from_json(
        {
            "number": 639,
            "title": "Improving License Clarity with Better Package Metadata",
            "authors": "Philippe Ombredanne, C.A.M. Gerlach, Karolina Surma",
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
    PEP.from_json(
        {
            "number": 213,
            "title": "Attribute Access Handlers",
            "authors": "Paul Prescod",
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
    PEP.from_json(
        {
            "number": 204,
            "title": "Range Literals",
            "authors": "Thomas Wouters",
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
    PEP.from_json(
        {
            "number": 3,
            "title": "Guidelines for Handling Bug Reports",
            "authors": "Jeremy Hylton",
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
    PEP.from_json(
        {
            "number": 100,
            "title": "Python Unicode Integration",
            "authors": "Marc-Andr\u00e9 Lemburg",
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
    PEP.from_json(
        {
            "number": 5,
            "title": "Guidelines for Language Evolution",
            "authors": "Paul Prescod",
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
    assert sorted(PEPs(SAMPLE_PEPS).statuses) == sorted(
        StatusCount(status, 1) for status in get_args(PEPStatus)
    )


##############################################################################
def test_type_counts() -> None:
    """We should eb able to count the types."""
    assert sorted(PEPs(SAMPLE_PEPS).types) == sorted(
        TypeCount(pep_type, 2) for pep_type in get_args(PEPType)
    )


### test_peps.py ends here
