"""Provides the main messages for the application."""

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual.message import Message

##############################################################################
# Local imports.
from ...peps import PEPStatus, PEPType


##############################################################################
class ShowAll(Message):
    """Message that requests that all PEPs be shown."""


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


### main.py ends here
