"""Provides the main application class."""

##############################################################################
# Textual imports.
from textual.app import InvalidThemeError

##############################################################################
# Textual enhanced imports.
from textual_enhanced.app import EnhancedApp

##############################################################################
# Local imports.
from .. import __version__
from .data import (
    load_configuration,
    update_configuration,
)
from .screens import Main


##############################################################################
class Peplum(EnhancedApp[None]):
    """The main application class."""

    HELP_TITLE = f"Peplum {__version__}"
    HELP_ABOUT = """
    `Peplum` is a terminal-based Python PEP lookup manager; it was created
    by and is maintained by [Dave Pearson](https://www.davep.org/); it is
    Free Software and can be [found on
    GitHub](https://github.com/davep/peplum).
    """
    HELP_LICENSE = """
    Peplum - The PEP lookup manager for the terminal.  \n    Copyright (C) 2025 Dave Pearson

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
    more details.

    You should have received a copy of the GNU General Public License along with
    this program. If not, see <https://www.gnu.org/licenses/>.
    """

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
