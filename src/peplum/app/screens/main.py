"""Provides the main screen for the application."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import Footer, Header

from peplum.app.commands.navigation_sorting import TogglePythonVersionsSortOrder

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
from ..messages import ShowAll, ShowAuthor, ShowPythonVersion, ShowStatus, ShowType
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
        }

        .focus {
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
            width: 1fr;
            height: 1fr;
            padding-right: 0;
            scrollbar-gutter: stable;
            &> .option-list--option {
                padding: 0 1;
            }
        }

        #content {
            width: 4fr;

            PEPsView {
                padding-right: 0;
                height: 1fr;
                border: none;
            }

            PEPDetails {
                display: none;
                height: auto;
                border-title-color: $text-primary;
                border-top: panel $border 50%;
                &:focus {
                    border-title-color: $text;
                    border-top: panel $border;
                }
                &.visible {
                    display: block;
                }
            }
        }
    }
    """

    COMMAND_MESSAGES = (
        # Keep these together as they're bound to function keys and destined
        # for the footer.
        Help,
        # Everything else.
        ChangeTheme,
        Escape,
        Quit,
        TogglePEPDetails,
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
            yield Navigation(load_configuration(), classes="panel focus").data_bind(
                Main.all_peps, Main.active_peps
            )
            with Vertical(id="content", classes="panel"):
                yield PEPsView(classes="focus").data_bind(Main.active_peps)
                yield PEPDetails(classes="focus").data_bind(pep=Main.selected_pep)
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
        else:
            self.app.exit()

    @on(TogglePEPDetails)
    def action_toggle_pep_details_command(self) -> None:
        """Toggle the display of the PEP details panel."""
        self.query_one(PEPDetails).toggle_class("visible")

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


### main.py ends here
