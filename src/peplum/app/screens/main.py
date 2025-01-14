"""Provides the main screen for the application."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header


##############################################################################
class Main(Screen[None]):
    """The main screen for the application."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        yield Footer()


### main.py ends here
