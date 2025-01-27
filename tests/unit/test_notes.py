"""Test the PEP notes class."""

##############################################################################
# Local imports.
from peplum.app.data.notes import Notes


##############################################################################
def test_empty_notes() -> None:
    """An empty notes object should have no length."""
    assert len(Notes()) == 0


##############################################################################
def test_one_note() -> None:
    """We should be able to add a note."""
    notes = Notes()
    notes[42] = "Life"
    assert len(notes) == 1


##############################################################################
def test_delete_a_note() -> None:
    """Should be able to delete a note."""
    notes = Notes()
    notes[42] = "Life"
    del notes[42]
    assert len(notes) == 0


##############################################################################
def test_blanking_a_note_is_removing_a_note() -> None:
    """If you blank out a note, it's the same as removing a note.."""
    notes = Notes()
    notes[42] = "Life"
    notes[42] = ""
    assert len(notes) == 0


##############################################################################
def test_notes_contains() -> None:
    """We should be able to see if there is a note."""
    notes = Notes()
    notes[1] = "Yes"
    notes[2] = ""
    assert 1 in notes
    assert 2 not in notes


##############################################################################
def test_getting_a_note_that_does_not_exist() -> None:
    """Getting a note that doesn't exist should get a blank note."""
    assert Notes()[42] == ""


### test_notes.py ends here
