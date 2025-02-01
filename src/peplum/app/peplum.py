"""Provides the main application class."""

##############################################################################
# Textual imports.
from textual.app import InvalidThemeError

##############################################################################
# Textual enhanced imports.
from textual_enhanced.app import EnhancedApp

##############################################################################
# Local imports.
from .data import (
    load_configuration,
    update_configuration,
)
from .screens import Main


##############################################################################
class Peplum(EnhancedApp[None]):
    """The main application class."""

    COMMANDS = set()

    def __init__(self) -> None:
        """Initialise the application."""
        super().__init__()
        configuration = load_configuration()
        if configuration.theme is not None:
            try:
                self.theme = configuration.theme
            except InvalidThemeError:
                pass

    def watch_theme(self) -> None:
        """Save the application's theme when it's changed."""
        with update_configuration() as config:
            config.theme = self.theme

    def on_mount(self) -> None:
        """Display the main screen."""
        self.push_screen(Main())


### peplum.py ends here
