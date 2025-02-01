"""Commands related to finding things."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command


##############################################################################
class FindPEP(Command):
    """Find and jump to a specific PEP"""

    BINDING_KEY = "p"


### finding.py ends here
