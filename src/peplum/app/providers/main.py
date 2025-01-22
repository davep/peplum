"""Provides the main application commands for the command palette."""

##############################################################################
# Local imports.
from ..commands import (
    ChangeTheme,
    Escape,
    Help,
    Quit,
    RedownloadPEPs,
    ShowAll,
    ToggleAuthorsSortOrder,
    TogglePEPDetails,
    TogglePythonVersionsSortOrder,
    ToggleStatusesSortOrder,
    ToggleTypesSortOrder,
)
from .commands_provider import CommandHits, CommandsProvider


##############################################################################
class MainCommands(CommandsProvider):
    """Provides some top-level commands for the application."""

    def commands(self) -> CommandHits:
        """Provide the main application commands for the command palette.

        Yields:
            The commands for the command palette.
        """
        yield ChangeTheme()
        yield Escape()
        yield Help()
        yield Quit()
        yield RedownloadPEPs()
        yield ShowAll()
        yield ToggleAuthorsSortOrder()
        yield TogglePEPDetails()
        yield TogglePythonVersionsSortOrder()
        yield ToggleStatusesSortOrder()
        yield ToggleTypesSortOrder()


### main.py ends here
