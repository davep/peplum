"""Provides the main screen for the application."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Header

##############################################################################
# Local imports.
from ... import __version__
from ..widgets import Navigation


##############################################################################
class Main(Screen[None]):
    """The main screen for the application."""

    TITLE = f"Peplum v{__version__}"

    DEFAULT_CSS = """
    Main {
        Navigation {
            width: 2fr;
            height: 1fr;
            &> .option-list--option {
                padding: 0 1;
            }
        }

        .focus {
            padding-right: 0;
            border: none;
            border-left: round $border 50%;
            background: $surface;
            scrollbar-gutter: stable;
            scrollbar-background: $surface;
            scrollbar-background-hover: $surface;
            scrollbar-background-active: $surface;
            &:focus, &:focus-within {
                border: none;
                border-left: round $border;
                background: $panel 80%;
                scrollbar-background: $panel;
                scrollbar-background-hover: $panel;
                scrollbar-background-active: $panel;
            }
        }
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with Horizontal():
            yield Navigation(classes="focus")
        yield Footer()


### main.py ends here
