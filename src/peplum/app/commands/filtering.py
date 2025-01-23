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
class Search(Command):
    """Search for text anywhere in the PEPs"""

    BINDING_KEY = "/"
    SHOW_IN_FOOTER = False


##############################################################################
class SearchAuthor(Command):
    """Search for an author then filter by them"""

    BINDING_KEY = "u"
    SHOW_IN_FOOTER = False


##############################################################################
class SearchPythonVersion(Command):
    """Search for a Python version and then filter by it"""

    BINDING_KEY = "v"
    SHOW_IN_FOOTER = False


##############################################################################
class SearchStatus(Command):
    """Search for a PEP status and then filter by it"""

    BINDING_KEY = "s"
    SHOW_IN_FOOTER = False


##############################################################################
class SearchType(Command):
    """Search for a PEP type and then filter by it"""

    BINDING_KEY = "t"
    SHOW_IN_FOOTER = False


### filtering.py ends here
