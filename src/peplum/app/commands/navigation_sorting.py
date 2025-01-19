"""Commands for affecting navigation sort ordering."""

##############################################################################
# Local imports.
from .base import Command


##############################################################################
class ToggleTypesSortOrder(Command):
    """Toggle the sort order of types in the navigation panel"""

    BINDING_KEY = "t"
    SHOW_IN_FOOTER = False


##############################################################################
class ToggleStatusesSortOrder(Command):
    """Toggle the sort order of the statuses in the navigation panel"""

    BINDING_KEY = "s"
    SHOW_IN_FOOTER = False


##############################################################################
class TogglePythonVersionsSortOrder(Command):
    """Toggle the sort order of Python versions in the navigation panel"""

    BINDING_KEY = "v"
    SHOW_IN_FOOTER = False


### navigation_sorting.py ends here
