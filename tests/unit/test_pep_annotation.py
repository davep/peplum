"""Test annotating a PEP."""

##############################################################################
# Pytest imports.
from pytest import fixture

##############################################################################
# Local imports.
from peplum.app.data import PEP


##############################################################################
@fixture
def example_pep() -> PEP:
    """An example PEP to work from."""
    return PEP.from_api(
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
    )


##############################################################################
def test_no_annotation(example_pep: PEP) -> None:
    """Annotating with nothing should do nothing."""
    assert id(example_pep.annotate()) == id(example_pep)


##############################################################################
def test_an_annotation(example_pep: PEP) -> None:
    """Annotating with new values result in a new instance of the PEP."""
    assert id(example_pep.annotate(notes="Changed")) != id(example_pep)


##############################################################################
def test_add_note(example_pep: PEP) -> None:
    """A note added to a PEP should be in the PEP."""
    assert example_pep.annotate(notes="test").notes == "test"


### test_pep_annotation.py ends here
