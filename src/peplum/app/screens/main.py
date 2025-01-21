"""Provides the main screen for the application."""

##############################################################################
# Python imports.
from webbrowser import open as visit_url

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import Footer, Header

##############################################################################
# Local imports.
from ... import __version__
from ...peps import PEP
from ..commands import (
    ChangeTheme,
    Command,
    Escape,
    Help,
    Quit,
    ToggleAuthorsSortOrder,
    TogglePEPDetails,
    TogglePythonVersionsSortOrder,
    ToggleStatusesSortOrder,
    ToggleTypesSortOrder,
)
from ..data import (
    PEPs,
    WithAuthor,
    WithPythonVersion,
    WithStatus,
    WithType,
    load_configuration,
    update_configuration,
)
from ..messages import (
    GotoPEP,
    ShowAll,
    ShowAuthor,
    ShowPythonVersion,
    ShowStatus,
    ShowType,
    VisitPEP,
)
from ..providers import MainCommands
from ..widgets import Navigation, PEPDetails, PEPsView
from .help import HelpScreen


##############################################################################
class Main(Screen[None]):
    """The main screen for the application."""

    TITLE = f"Peplum v{__version__}"

    HELP = """
    ## Main application keys and commands

    The following keys and commands can be used anywhere here on the main screen.
    """

    DEFAULT_CSS = """
    Main {
        .panel {
            border: none;
            border-left: round $border 50%;
            &:focus, &:focus-within {
                border: none;
                border-left: round $border;
            }
            background: $surface;
            scrollbar-background: $surface;
            scrollbar-background-hover: $surface;
            scrollbar-background-active: $surface;
            &:focus, &:focus-within {
                background: $panel 80%;
                scrollbar-background: $panel;
                scrollbar-background-hover: $panel;
                scrollbar-background-active: $panel;
            }
        }

        Navigation {
            width: 2fr;
            height: 1fr;
            padding-right: 0;
            scrollbar-gutter: stable;
            &> .option-list--option {
                padding: 0 1;
            }
        }

        PEPsView {
            width: 8fr;
            height: 1fr;
            padding-right: 0;
            border: none;
        }

        PEPDetails {
            width: 3fr;
            display: none;
            height: 1fr;
            border-title-color: $text-primary;
            border-top: panel $border 50%;
            &:focus {
                border-title-color: $text;
                border-top: panel $border;
            }
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
        TogglePEPDetails,
        Quit,
        # Everything else.
        ChangeTheme,
        Escape,
        ToggleAuthorsSortOrder,
        TogglePythonVersionsSortOrder,
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

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with Horizontal():
            yield Navigation(load_configuration(), classes="panel").data_bind(
                Main.all_peps, Main.active_peps
            )
            yield PEPsView(classes="panel").data_bind(Main.active_peps)
            yield PEPDetails(classes="panel").data_bind(pep=Main.selected_pep)
        yield Footer()

    def on_mount(self) -> None:
        """Configure the application once the DOM is mounted."""
        # TODO: Get from the API.
        # TODO: Do this as a background process.
        # self.all_peps = PEPs(await API().get_peps())
        from json import loads
        from pathlib import Path

        self.all_peps = PEPs(
            PEP.from_json(pep)
            for pep in loads(Path("/Users/davep/peps.json").read_text()).values()
        )
        self.set_class(load_configuration().details_visble, "details-visible")

    def watch_all_peps(self) -> None:
        """React to the full set of PEPs being updated."""
        self.active_peps = self.all_peps

    def watch_active_peps(self) -> None:
        """React to the active PEPs being updated."""
        self.sub_title = f"{self.active_peps.description} ({len(self.active_peps)})"

    @on(PEPsView.PEPHighlighted)
    def select_pep(self, message: PEPsView.PEPHighlighted) -> None:
        """Make the currently-selected PEP the one to view."""
        self.selected_pep = message.pep

    @on(ShowAll)
    def show_all(self) -> None:
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


### main.py ends here
