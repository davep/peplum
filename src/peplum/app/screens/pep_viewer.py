"""A dialog for viewing the text of a PEP."""

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
from ..data import PEP


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
        }

        #text {
            padding: 0 1;
        }

        #buttons {
            height: auto;
            margin-top: 1;
            align-horizontal: right;
        }

        Button {
            margin-right: 1;
        }
    }
    """

    BINDINGS = [("escape", "close")]

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
                yield Button("Close [dim]\\[Esc][/]")

    @work
    async def _download_text(self) -> None:
        """Download the text of the PEP."""
        try:
            self.query_one("#text", Static).update(
                await API().get_pep(self._pep.number)
            )
        except API.RequestError as error:
            self.query_one("#text", Static).update("[error]Error[/]")
            self.notify(
                str(error), title="Error downloading PEP source", severity="error"
            )
            return
        finally:
            self.query_one("#viewer").loading = False
        self.set_focus(self.query_one("#viewer"))

    def on_mount(self) -> None:
        """Populate the dialog once the"""
        self.query_one("#viewer").loading = True
        self._download_text()

    @on(Button.Pressed)
    def action_close(self) -> None:
        """Close the dialog."""
        self.dismiss(None)


### pep_viewer.py ends here
