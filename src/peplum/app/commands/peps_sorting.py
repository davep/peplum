"""Provides command-oriented messages that relate to sorting PEPs."""

##############################################################################
# Local imports.
from .base import Command


##############################################################################
class SortByNumber(Command):
    """Sort PEPs by their number"""

    BINDING_KEY = "1"
    SHOW_IN_FOOTER = False


##############################################################################
class SortByCreated(Command):
    """Sort PEPs by their created date"""

    BINDING_KEY = "2"
    SHOW_IN_FOOTER = False


##############################################################################
class SortByTitle(Command):
    """Sort PEPs by their title"""

    BINDING_KEY = "3"
    SHOW_IN_FOOTER = False


### peps_sorting.py ends here
