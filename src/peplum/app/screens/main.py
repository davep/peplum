"""Provides the main screen for the application."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import Footer, Header

##############################################################################
# Local imports.
from ... import __version__
from ...peps import API
from ..data import PEPs
from ..widgets import Navigation, PEPsView


##############################################################################
class Main(Screen[None]):
    """The main screen for the application."""

    TITLE = f"Peplum v{__version__}"

    DEFAULT_CSS = """
    Main {
        Navigation {
            width: 1fr;
        }

        PEPsView {
            width: 4fr;
        }

        Navigation, PEPsView {
            &> .option-list--option {
                padding: 0 1;
            }
            height: 1fr;
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

    all_peps: var[PEPs] = var(PEPs)
    """All the PEPs that we know about."""

    active_peps: var[PEPs] = var(PEPs)
    """The currently-active set of PEPs."""

    def compose(self) -> ComposeResult:
        """Compose the content of the main screen."""
        yield Header()
        with Horizontal():
            yield Navigation().data_bind(peps=Main.active_peps)
            yield PEPsView().data_bind(peps=Main.active_peps)
        yield Footer()

    async def on_mount(self) -> None:
        """Configure the application once the DOM is mounted."""
        # TODO: Get from the API.
        # TODO: Do this as a background process.
        # self.all_peps = PEPs(await API().get_peps())
        from json import loads
        from pathlib import Path

        from peplum.peps import PEP

        self.all_peps = PEPs(
            PEP.from_json(pep)
            for pep in loads(Path("/Users/davep/peps.json").read_text()).values()
        )

    def watch_all_peps(self) -> None:
        """React to the full set of PEPs being updated."""
        self.active_peps = self.all_peps


### main.py ends here
