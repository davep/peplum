"""Provides command-oriented messages that relate to filtering."""

##############################################################################
# Local imports.
from .base import Command


##############################################################################
class ShowAll(Command):
    """Clear any filters and show all PEPs"""

    BINDING_KEY = "a"
    SHOW_IN_FOOTER = False


##############################################################################
class SearchAuthor(Command):
    """Search for an author then filter by them"""

    BINDING_KEY = "u"
    SHOW_IN_FOOTER = False


### filtering.py ends here
