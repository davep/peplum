"""Provides the main application commands for the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import CommandHits, CommandsProvider

##############################################################################
# Local imports.
from ..commands import (
    ChangeTheme,
    EditNotes,
    Escape,
    FindPEP,
    Help,
    Quit,
    RedownloadPEPs,
    Search,
    SearchAuthor,
    SearchPythonVersion,
    SearchStatus,
    SearchType,
    ShowAll,
    SortByCreated,
    SortByNumber,
    SortByTitle,
    ToggleAuthorsSortOrder,
    TogglePEPDetails,
    TogglePythonVersionsSortOrder,
    ToggleStatusesSortOrder,
    ToggleTypesSortOrder,
    ViewPEP,
)


##############################################################################
class MainCommands(CommandsProvider):
    """Provides some top-level commands for the application."""

    def commands(self) -> CommandHits:
        """Provide the main application commands for the command palette.

        Yields:
            The commands for the command palette.
        """
        yield ChangeTheme()
        yield EditNotes()
        yield Escape()
        yield FindPEP()
        yield Help()
        yield Quit()
        yield RedownloadPEPs()
        yield Search()
        yield SearchAuthor()
        yield SearchPythonVersion()
        yield SearchStatus()
        yield SearchType()
        yield ShowAll()
        yield SortByCreated()
        yield SortByNumber()
        yield SortByTitle()
        yield ToggleAuthorsSortOrder()
        yield TogglePEPDetails()
        yield TogglePythonVersionsSortOrder()
        yield ToggleStatusesSortOrder()
        yield ToggleTypesSortOrder()
        yield ViewPEP()


### main.py ends here
