"""Commands related to finding things."""

##############################################################################
# Local imports.
from .base import Command


##############################################################################
class FindPEP(Command):
    """Find and jump to a specific PEP"""

    BINDING_KEY = "p"
    SHOW_IN_FOOTER = False


### finding.py ends here
