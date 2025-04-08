"""Provides the main screen for the application."""

##############################################################################
# Python imports.
from argparse import Namespace
from dataclasses import dataclass
from json import dumps, loads
from webbrowser import open as visit_url

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import var
from textual.widgets import Footer, Header

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import Command, Help, Quit
from textual_enhanced.dialogs import HelpScreen, ModalInput
from textual_enhanced.screen import EnhancedScreen

##############################################################################
# Local imports.
from ... import __version__
from ...peps import API
from ..commands import (
    ChangeTheme,
    EditNotes,
    Escape,
    FindPEP,
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
    ToggleSortOrder,
    ToggleStatusesSortOrder,
    ToggleTypesSortOrder,
    ViewPEP,
)
from ..data import (
    PEP,
    Containing,
    Notes,
    PEPs,
    WithAuthor,
    WithPythonVersion,
    WithStatus,
    WithType,
    load_configuration,
    pep_data,
    update_configuration,
)
from ..messages import (
    GotoPEP,
    ShowAuthor,
    ShowPythonVersion,
    ShowStatus,
    ShowType,
    VisitPEP,
)
from ..providers import (
    AuthorCommands,
    MainCommands,
    PEPsCommands,
    PythonVersionCommands,
    StatusCommands,
    TypeCommands,
)
from ..widgets import Navigation, PEPDetails, PEPsView
from .notes_editor import NotesEditor
from .pep_viewer import PEPViewer


##############################################################################
class Main(EnhancedScreen[None]):
    """The main screen for the application."""

    TITLE = f"Peplum v{__version__}"

    HELP = """
    ## Main application keys and commands

    The following keys and commands can be used anywhere here on the main screen.
    """

    DEFAULT_CSS = """
    Main {
        layout: horizontal;

        .panel {
            height: 1fr;
            border: none;
            border-left: round $border 50%;
            background: $surface;
            padding-right: 0;
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
            & > .option-list--option {
                padding: 0 1;
            }
        }

        Navigation {
            width: 2fr;
        }

        PEPsView {
            width: 8fr;
            scrollbar-gutter: stable;
        }

        PEPDetails {
            width: 3fr;
            display: none;
        }

        &.details-visible {
            PEPsView {
                width: 5fr;
            }
            PEPDetails {
                display: block;
            }
        }
    }
    """

    COMMAND_MESSAGES = (
        # Keep these together as they're bound to function keys and destined
        # for the footer.
        Help,
        EditNotes,
        TogglePEPDetails,
        ViewPEP,
        Quit,
        RedownloadPEPs,
        # Everything else.
        ChangeTheme,
        Escape,
        FindPEP,
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
        TogglePythonVersionsSortOrder,
        ToggleSortOrder,
        ToggleStatusesSortOrder,
        ToggleTypesSortOrder,
    )

    BINDINGS = Command.bindings(*COMMAND_MESSAGES)

    COMMANDS = {MainCommands}

    all_peps: var[PEPs] = var(PEPs)
    """All the PEPs that we know about."""

    active_peps: var[PEPs] = var(PEPs)
    """The currently-active set of PEPs."""

    selected_pep: var[PEP | None] = var(None)
    """The currently-selected PEP."""

    notes: var[Notes] = var(Notes)
    """The user's notes about PEPs."""

    def __init__(self, arguments: Namespace) -> None:
        """Initialise the main screen.

        Args:
            arguments: The arguments passed to the application on the command line.
        """
        self._arguments = arguments
        """The arguments passed on the command line."""
        super().__init__()
        self._jump_to_on_load: str | None = self._arguments.pep
        """A PEP to jump to once the display is loaded."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        yield Navigation(load_configuration(), classes="panel").data_bind(
            Main.all_peps, Main.active_peps
        )
        yield PEPsView(classes="panel").data_bind(Main.active_peps)
        yield PEPDetails(classes="panel").data_bind(pep=Main.selected_pep)
        yield Footer()

    @dataclass
    class Loaded(Message):
        """A message sent when PEP data is loaded."""

        peps: PEPs
        """The PEP data that was loaded."""

    @work(thread=True)
    def load_pep_data(self) -> None:
        """Load the local copy of the PEP data."""
        if not pep_data().exists():
            return
        try:
            self.notes.load()
            self.post_message(
                self.Loaded(
                    PEPs(
                        PEP.from_storage(pep, self.notes)
                        for pep in loads(pep_data().read_text()).values()
                    )
                )
            )
        except IOError as error:
            self.notify(str(error), title="Error loading PEP data", severity="error")

    @work(thread=True)
    async def download_pep_data(self) -> None:
        """Download a fresh copy of the PEP data."""
        # Get the raw data from the API.
        try:
            raw_data = await API().get_peps()
        except API.Error as error:
            self.notify(str(error), title="API Error", severity="error", timeout=8)
            return
        # Store the raw data.
        try:
            pep_data().write_text(dumps(raw_data, indent=4), encoding="utf-8")
        except IOError as error:
            self.notify(str(error), title="Error saving PEP data", severity="error")
            return
        # Now kick off loading the raw data.
        self.notify("Fresh PEP data downloaded from the PEP API")
        self.load_pep_data()

    @staticmethod
    def _extract_pep(pep: str) -> int | None:
        """Try and extract a PEP number from a string.

        Args:
            pep: A string that should contain a PEP number.

        Returns:
            A PEP number or [`None`][None] if one could not be found.

        Notes:
            The likes of `2342` and `PEP2342` are handled.
        """
        try:
            return int(pep.strip().upper().removeprefix("PEP"))
        except ValueError:
            return None

    @on(Loaded)
    def load_fresh_peps(self, message: Loaded) -> None:
        """React to a fresh set of PEPs being made available.

        Args:
            message: The message letting us know we have fresh PEPs.
        """
        if len(message.peps.authors) == 0:
            self.notify(
                "You likely have a cached copy of the older version of the PEP data; a redownload is recommended.",
                severity="warning",
                timeout=8,
            )
        config = load_configuration()
        self.all_peps = message.peps.sorted_by(config.peps_sort_order).reversed(
            config.peps_sort_reversed
        )
        if self._jump_to_on_load is not None:
            if (pep := self._extract_pep(self._jump_to_on_load)) is not None:
                self.post_message(GotoPEP(pep))
            self._jump_to_on_load = None

    def on_mount(self) -> None:
        """Configure the application once the DOM is mounted."""
        # The caller has passed sorting preferences on the command line;
        # let's get them into the configuration before anything else kicks
        # off.
        if self._arguments.sort_by is not None:
            with update_configuration() as config:
                config.peps_sort_reversed = self._arguments.sort_by[0] == "~"
                config.peps_sort_order = self._arguments.sort_by.removeprefix("~")
        self.set_class(load_configuration().details_visble, "details-visible")
        # On startup, if we've got local PEP data...
        if pep_data().exists():
            # ...load and display that.
            self.load_pep_data()
        else:
            # Given we've got no local data at all, let's force an attempt
            # to download from the API.
            self.download_pep_data()

    def watch_all_peps(self) -> None:
        """React to the full set of PEPs being updated."""
        self.active_peps = self.all_peps
        PEPsCommands.peps = self.all_peps

    def watch_active_peps(self) -> None:
        """React to the active PEPs being updated."""
        self.sub_title = f"{self.active_peps.description} ({len(self.active_peps)})"
        AuthorCommands.active_peps = self.active_peps
        PythonVersionCommands.active_peps = self.active_peps
        StatusCommands.active_peps = self.active_peps
        TypeCommands.active_peps = self.active_peps

    @on(PEPsView.PEPHighlighted)
    def select_pep(self, message: PEPsView.PEPHighlighted) -> None:
        """Make the currently-selected PEP the one to view."""
        self.selected_pep = message.pep

    @on(PEPsView.Empty)
    def deselect_pep(self) -> None:
        """Handle there being no highlighted PEP."""
        self.selected_pep = None

    @on(ShowAll)
    def action_show_all_command(self) -> None:
        """Show all PEPs."""
        self.active_peps = self.all_peps

    @on(ShowType)
    def show_type(self, command: ShowType) -> None:
        """Filter the PEPs by a given type.

        Args:
            command: The command requesting the filter.
        """
        self.active_peps &= WithType(command.type)

    @on(ShowStatus)
    def show_status(self, command: ShowStatus) -> None:
        """Filter the PEPs by a given status.

        Args:
            command: The command requesting the filter.
        """
        self.active_peps &= WithStatus(command.status)

    @on(ShowPythonVersion)
    def show_python_version(self, command: ShowPythonVersion) -> None:
        """Filter the PEPs by a given Python version.

        Args:
            command: The command requesting the filter.
        """
        self.active_peps &= WithPythonVersion(command.version)

    @on(ShowAuthor)
    def show_author(self, command: ShowAuthor) -> None:
        """Filter the PEPs by a given author.

        Args:
            command: The command requesting the filter.
        """
        self.active_peps &= WithAuthor(command.author)

    @on(GotoPEP)
    def goto_pep(self, command: GotoPEP) -> None:
        """Visit a specific PEP by its number.

        Args:
            command: The command requesting the PEP by number.
        """
        if command.number in self.active_peps:
            self.query_one(PEPsView).goto_pep(command.number)
        elif command.number in self.all_peps:
            self.notify(
                f"PEP{command.number} wasn't in the active filter; switching to all PEPs...",
                severity="warning",
            )
            self.active_peps = self.all_peps
            self.call_after_refresh(self.query_one(PEPsView).goto_pep, command.number)
        else:
            self.notify(
                f"PEP{command.number} doesn't exist. Perhaps you'll be the one to write it?",
                title="No such PEP",
                severity="error",
            )

    @on(VisitPEP)
    def visit_pep(self, command: VisitPEP) -> None:
        """Visit a given PEP's webpage.

        Args:
            command: The command requesting the visit.
        """
        if command.pep.url:
            visit_url(command.pep.url)
        else:
            self.notify(f"PEP{command.pep.number} has no associated URL")

    @on(FindPEP)
    def action_find_pep_command(self) -> None:
        """Find a PEP and jump to it."""
        self.show_palette(PEPsCommands)

    @on(Search)
    @work
    async def action_search_command(self) -> None:
        """Free-text search within the PEPs."""
        if search_text := await self.app.push_screen_wait(
            ModalInput("Case-insensitive text to look for in the PEPs")
        ):
            self.active_peps = self.active_peps & Containing(search_text)

    @on(SearchAuthor)
    def action_search_author_command(self) -> None:
        """Search for an author and use them as a filter."""
        self.show_palette(AuthorCommands)

    @on(SearchPythonVersion)
    def action_search_python_version_command(self) -> None:
        """Search for a Python version and then use it as a filter."""
        self.show_palette(PythonVersionCommands)

    @on(SearchStatus)
    def action_search_status_command(self) -> None:
        """Search for a status and use it as a filter."""
        self.show_palette(StatusCommands)

    @on(SearchType)
    def action_search_type_command(self) -> None:
        """Search for a PEP type and then use it as a filter."""
        self.show_palette(TypeCommands)

    @on(RedownloadPEPs)
    def action_redownload_peps_command(self) -> None:
        """Redownload PEPs from the API."""
        self.download_pep_data()

    @on(Help)
    def action_help_command(self) -> None:
        """Toggle the display of the help panel."""
        self.app.push_screen(HelpScreen(self))

    @on(ChangeTheme)
    def action_change_theme_command(self) -> None:
        """Show the theme picker."""
        self.app.search_themes()

    @on(Quit)
    def action_quit_command(self) -> None:
        """Quit the application."""
        self.app.exit()

    @on(Escape)
    def action_escape_command(self) -> None:
        """Handle escaping.

        The action's approach is to step-by-step back out from the 'deepest'
        level to the topmost, and if we're at the topmost then exit the
        application.
        """
        if self.focused == self.query_one(PEPsView):
            self.set_focus(self.query_one(Navigation))
        elif (
            self.focused
            and self.query_one(PEPDetails) in self.focused.ancestors_with_self
        ):
            self.set_focus(self.query_one(PEPsView))
        else:
            self.app.exit()

    @on(TogglePEPDetails)
    def action_toggle_pep_details_command(self) -> None:
        """Toggle the display of the PEP details panel."""
        self.toggle_class("details-visible")
        with update_configuration() as config:
            config.details_visble = self.has_class("details-visible")

    @on(ToggleTypesSortOrder)
    def action_toggle_types_sort_order_command(self) -> None:
        """Toggle the sort order of the types."""
        with update_configuration() as config:
            config.sort_types_by_count = not config.sort_types_by_count
            self.query_one(Navigation).sort_types_by_count = config.sort_types_by_count

    @on(ToggleStatusesSortOrder)
    def action_toggle_statuses_sort_order_command(self) -> None:
        """Toggle the sort order of the statuses."""
        with update_configuration() as config:
            config.sort_statuses_by_count = not config.sort_statuses_by_count
            self.query_one(
                Navigation
            ).sort_statuses_by_count = config.sort_statuses_by_count

    @on(TogglePythonVersionsSortOrder)
    def action_toggle_python_versions_sort_order_command(self) -> None:
        """Toggle the sort order of the Python Versions."""
        with update_configuration() as config:
            config.sort_python_versions_by_count = (
                not config.sort_python_versions_by_count
            )
            self.query_one(
                Navigation
            ).sort_python_versions_by_count = config.sort_python_versions_by_count

    @on(ToggleAuthorsSortOrder)
    def action_toggle_authors_sort_order_command(self) -> None:
        """Toggle the sort order of the authors."""
        with update_configuration() as config:
            config.sort_authors_by_count = not config.sort_authors_by_count
            self.query_one(
                Navigation
            ).sort_authors_by_count = config.sort_authors_by_count

    @on(SortByCreated)
    def action_sort_by_created_command(self) -> None:
        """Sort the PEPs by their date created."""
        with update_configuration() as config:
            config.peps_sort_order = "created"
            self.active_peps = self.active_peps.sorted_by(config.peps_sort_order)

    @on(SortByNumber)
    def action_sort_by_number_command(self) -> None:
        """Sort the PEPs by their number."""
        with update_configuration() as config:
            config.peps_sort_order = "number"
            self.active_peps = self.active_peps.sorted_by(config.peps_sort_order)

    @on(SortByTitle)
    def action_sort_by_title_command(self) -> None:
        """Sort the PEPs by their title."""
        with update_configuration() as config:
            config.peps_sort_order = "title"
            self.active_peps = self.active_peps.sorted_by(config.peps_sort_order)

    @on(ToggleSortOrder)
    def action_toggle_sort_order_command(self) -> None:
        """Toggle the current sort order direction of the PEPs."""
        with update_configuration() as config:
            config.peps_sort_reversed = not config.peps_sort_reversed
            self.active_peps = self.active_peps.reversed(config.peps_sort_reversed)

    @work(thread=True)
    def _save_notes(self) -> None:
        """Save the notes."""
        try:
            self.notes.save()
        except IOError as error:
            self.notify(
                str(error), title="Unable to save notes", severity="error", timeout=8
            )

    @on(EditNotes)
    @work
    async def action_edit_notes_command(self) -> None:
        """Edit the notes for the currently-highlighted PEP."""
        if self.selected_pep is None:
            self.notify("Highlight a PEP to edit its notes.", severity="warning")
            return
        if (
            notes := await self.app.push_screen_wait(NotesEditor(self.selected_pep))
        ) is not None:
            self.notes[self.selected_pep.number] = notes
            self._save_notes()
            self.active_peps = self.active_peps.rebuild_from(
                self.all_peps.patch_pep(self.selected_pep.annotate(notes=notes))
            )

    @on(ViewPEP)
    def action_view_pep_command(self) -> None:
        """View the currently-highlighted PEP's source."""
        if self.selected_pep is None:
            self.notify("Highlight a PEP to view it.", severity="warning")
            return
        if self.selected_pep.number == 0:
            self.notify("PEP0 has no source to view.", severity="warning")
            return
        self.app.push_screen(PEPViewer(self.selected_pep))


### main.py ends here
