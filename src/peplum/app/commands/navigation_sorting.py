"""Commands for affecting navigation sort ordering."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class ToggleTypesSortOrder(Command):
    """Toggle the sort order of types in the navigation panel"""

    BINDING_KEY = "T"


##############################################################################
class ToggleStatusesSortOrder(Command):
    """Toggle the sort order of the statuses in the navigation panel"""

    BINDING_KEY = "S"


##############################################################################
class TogglePythonVersionsSortOrder(Command):
    """Toggle the sort order of Python versions in the navigation panel"""

    BINDING_KEY = "V"


##############################################################################
class ToggleAuthorsSortOrder(Command):
    """Toggle the sort order of the authors in the navigation panel"""

    BINDING_KEY = "A"


### navigation_sorting.py ends here
