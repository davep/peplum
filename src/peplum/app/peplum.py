"""Provides the main application class."""

##############################################################################
# Python imports.
from argparse import Namespace

##############################################################################
# Textual imports.
from textual.app import InvalidThemeError, ScreenStackError

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

    def __init__(self, arguments: Namespace) -> None:
        """Initialise the application.

        Args:
            The command line arguments passed to the application.
        """
        self._arguments = arguments
        """The command line arguments passed to the application."""
        super().__init__()
        configuration = load_configuration()
        if configuration.theme is not None:
            try:
                self.theme = arguments.theme or configuration.theme
            except InvalidThemeError:
                pass
        try:
            self.update_keymap(configuration.bindings)
        except ScreenStackError:  # https://github.com/Textualize/textual/issues/5742
            pass

    def watch_theme(self) -> None:
        """Save the application's theme when it's changed."""
        with update_configuration() as config:
            config.theme = self.theme

    def get_default_screen(self) -> Main:
        """Get the default screen for the application.

        Returns:
            The main screen.
        """
        return Main(self._arguments)


### peplum.py ends here
