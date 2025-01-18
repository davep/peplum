"""Provides a widget for showing a PEP's details."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label, Rule


##############################################################################
class PEPDetails(VerticalScroll):
    """A widget for showing details of a PEP."""

    def compose(self) -> ComposeResult:
        yield Rule()
        yield Label("Something wonderful will happen")


### pep_details.py ends here
