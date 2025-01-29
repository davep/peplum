"""A dialog for viewing the text of a PEP."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Static

##############################################################################
# Local imports.
from ...peps import API
from ..data import PEP, cache_dir


##############################################################################
class PEPViewer(ModalScreen[None]):
    """A modal screen for viewing a PEP's source."""

    CSS = """
    PEPViewer {
        align: center middle;

        &> Vertical {
            width: 80%;
            height: 80%;
            max-height: 80%;
            background: $panel;
            border: panel $border;
        }

        #viewer {
            height: 1fr;
            scrollbar-background: $panel;
            scrollbar-background-hover: $panel;
            scrollbar-background-active: $panel;
            #text {
                padding: 0 1;
                color: $text-muted;
            }
            &:focus #text {
                color: $text;
            }
        }

        #buttons {
            height: auto;
            margin-top: 1;
            align-horizontal: right;
            border-top: round $border;
        }

        Button {
            margin-right: 1;
        }
    }
    """

    BINDINGS = [("escape", "close"), ("ctrl+r", "refresh")]

    def __init__(self, pep: PEP) -> None:
        """Initialise the dialog.

        Args:
            pep: The PEP to view.
        """
        super().__init__()
        self._pep = pep
        """The PEP to view."""

    def compose(self) -> ComposeResult:
        """Compose the dialog's content."""
        with Vertical() as dialog:
            dialog.border_title = f"PEP{self._pep.number}"
            yield VerticalScroll(Static(id="text"), id="viewer")
            with Horizontal(id="buttons"):
                yield Button("Refresh [dim]\\[^r][/]", id="refresh")
                yield Button("Close [dim]\\[Esc][/]", id="close")

    @property
    def _cache_name(self) -> Path:
        """The name of the file that is the cached version of the PEP source."""
        return cache_dir() / API.pep_file(self._pep.number)

    @work
    async def _download_text(self) -> None:
        """Download the text of the PEP.

        Notes:
            Once downloaded a local copy will be saved. Subsequently, when
            attempting to download the PEP, this local copy will be used
            instead.
        """
        self.query_one("#viewer").loading = True
        pep_source = ""

        if self._cache_name.exists():
            try:
                pep_source = self._cache_name.read_text(encoding="utf-8")
            except IOError:
                pass

        if not pep_source:
            try:
                self._cache_name.write_text(
                    pep_source := await API().get_pep(self._pep.number),
                    encoding="utf-8",
                )
            except IOError:
                pass
            except API.RequestError as error:
                pep_source = "Error downloading PEP source"
                self.notify(
                    str(error), title="Error downloading PEP source", severity="error"
                )

        self.query_one("#text", Static).update(pep_source)
        self.query_one("#viewer").loading = False
        self.set_focus(self.query_one("#viewer"))

    def on_mount(self) -> None:
        """Populate the dialog once the"""
        self._download_text()

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Close the dialog."""
        self.dismiss(None)

    @on(Button.Pressed, "#refresh")
    def action_refresh(self) -> None:
        """Refresh the PEP source."""
        try:
            self._cache_name.unlink(missing_ok=True)
        except IOError:
            pass
        self._download_text()


### pep_viewer.py ends here
