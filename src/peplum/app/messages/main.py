"""Provides the main messages for the application."""

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual.message import Message

##############################################################################
# Local imports.
from ..data import PEP, PEPStatus, PEPType


##############################################################################
@dataclass
class GotoPEP(Message):
    """Message that requests we go to a specific PEP."""

    number: int
    """The number of the PEP to go to."""


##############################################################################
@dataclass
class ShowType(Message):
    """Message that requests that PEPs of a certain type are shown."""

    type: PEPType
    """The PEP type to show."""


##############################################################################
@dataclass
class ShowStatus(Message):
    """Message that requests that PEPs of a certain status are shown."""

    status: PEPStatus
    """The status to show."""


##############################################################################
@dataclass
class ShowPythonVersion(Message):
    """Message that requests that PEPs of a certain Python version are shown."""

    version: str
    """The Python version to show."""


##############################################################################
@dataclass
class ShowAuthor(Message):
    """Message that requests that PEPs of a certain author are shown."""

    author: str
    """The author to show."""


##############################################################################
@dataclass
class VisitPEP(Message):
    """Message that makes a request to visit the URL of a given PEP."""

    pep: PEP
    """The PEP to visit."""


### main.py ends here
