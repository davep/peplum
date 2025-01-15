"""Provides a class for letting the user view a list of PEPs."""

##############################################################################
# Textual imports.
from textual.reactive import var
from textual.widgets.option_list import Option

##############################################################################
# Local imports.
from ..data import PEPs
from .extended_option_list import OptionListEx


##############################################################################
class PEPsView(OptionListEx):
    """A widget for viewing a list of PEPs."""

    peps: var[PEPs] = var(PEPs, always_update=True)
    """The currently-active collection of PEPs."""

    def watch_peps(self) -> None:
        """React to the PEPs being changed."""
        with self.preserved_highlight:
            self.clear_options().add_options(
                Option(f"{pep.number}: {pep.title}", id=f"{pep.number}")
                for pep in self.peps
            )


### peps_view.py ends here
