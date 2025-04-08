"""Provides command-oriented messages that relate to sorting PEPs."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class SortByNumber(Command):
    """Sort PEPs by their number"""

    BINDING_KEY = "1"


##############################################################################
class SortByCreated(Command):
    """Sort PEPs by their created date"""

    BINDING_KEY = "2"


##############################################################################
class SortByTitle(Command):
    """Sort PEPs by their title"""

    BINDING_KEY = "3"


##############################################################################
class ToggleSortOrder(Command):
    """Toggle the current sort order"""

    BINDING_KEY = "minus"


### peps_sorting.py ends here
