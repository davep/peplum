"""The main navigation panel."""

##############################################################################
# Textual imports.
from textual.reactive import var

##############################################################################
# Local imports.
from ..data import PEPs
from .extended_option_list import OptionListEx


##############################################################################
class Navigation(OptionListEx):
    """The main navigation panel."""

    peps: var[PEPs] = var(PEPs, always_update=True)
    """The currently-active collection of PEPs."""


### navigation.py ends here
