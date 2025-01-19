"""Provides the main application commands for the command palette."""

##############################################################################
# Local imports.
from ..commands import (
    ChangeTheme,
    Escape,
    Help,
    Quit,
    TogglePEPDetails,
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
        yield TogglePEPDetails()
        yield ToggleStatusesSortOrder()
        yield ToggleTypesSortOrder()


### main.py ends here
