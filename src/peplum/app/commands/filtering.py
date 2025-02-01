"""Provides command-oriented messages that relate to filtering."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class ShowAll(Command):
    """Clear any filters and show all PEPs"""

    BINDING_KEY = "a"


##############################################################################
class Search(Command):
    """Search for text anywhere in the PEPs"""

    BINDING_KEY = "/"


##############################################################################
class SearchAuthor(Command):
    """Search for an author then filter by them"""

    BINDING_KEY = "u"


##############################################################################
class SearchPythonVersion(Command):
    """Search for a Python version and then filter by it"""

    BINDING_KEY = "v"


##############################################################################
class SearchStatus(Command):
    """Search for a PEP status and then filter by it"""

    BINDING_KEY = "s"


##############################################################################
class SearchType(Command):
    """Search for a PEP type and then filter by it"""

    BINDING_KEY = "t"


### filtering.py ends here
