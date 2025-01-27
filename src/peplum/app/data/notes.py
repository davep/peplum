"""Provides a class for handling notes made about PEPs."""

##############################################################################
# Python imports.
from json import dumps, loads
from pathlib import Path
from typing import Final

##############################################################################
# Typing extension imports.
from typing_extensions import Self

##############################################################################
# Local imports.
from .locations import data_dir


##############################################################################
class Notes:
    """Class that holds the notes the user has made about PEPs."""

    _NOTES_FILE: Final[Path] = data_dir() / Path("notes.json")
    """The location of the notes file."""

    def __init__(self) -> None:
        """Initialise the object."""
        self._notes: dict[int, str] = {}
        """The notes."""

    def load(self, source: Path | None = None) -> Self:
        """Load the notes.

        Args:
            source: The optional source location to load the notes from.

        Returns:
            Self.
        """
        if (source := source or self._NOTES_FILE).exists():
            self._notes = {
                int(number): note
                for number, note in loads(source.read_text(encoding="utf-8")).items()
            }
        return self

    def save(self, target: Path | None = None) -> Self:
        """Save the notes.

        Args:
            target: The optional target location to save the notes to.

        Returns:
            Self.
        """
        (target or self._NOTES_FILE).write_text(
            dumps(self._notes, indent=4), encoding="utf-8"
        )
        return self

    def __getitem__(self, pep: int) -> str:
        """Get the note for a PEP."""
        return self._notes.get(pep, "")

    def __setitem__(self, pep: int, notes: str) -> None:
        """Set the note for a PEP."""
        if notes := notes.strip():
            self._notes[pep] = notes
        else:
            del self[pep]

    def __delitem__(self, pep: int) -> None:
        """Remove a note for a PEP."""
        try:
            del self._notes[pep]
        except KeyError:
            # Attempting to delete a note that doesn't exist is fine with
            # us.
            pass

    def __contains__(self, pep: int) -> bool:
        """Are there notes for a PEP?"""
        return bool(self._notes.get(pep))

    def __len__(self) -> int:
        """The count of notes."""
        return len(self._notes)


### notes.py ends here
