"""Commands for affecting navigation sort ordering."""

##############################################################################
# Local imports.
from .base import Command


##############################################################################
class ToggleTypesSortOrder(Command):
    """Toggle the sort order of types in the navigation panel"""

    BINDING_KEY = "t"
    SHOW_IN_FOOTER = False


### navigation_sorting.py ends here
