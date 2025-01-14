"""Provides the main screen for the application."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

##############################################################################
# Local imports.
from ... import __version__


##############################################################################
class Main(Screen[None]):
    """The main screen for the application."""

    TITLE = f"Peplum v{__version__}"

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        yield Footer()


### main.py ends here
