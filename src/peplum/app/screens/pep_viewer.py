"""A dialog for viewing the text of a PEP."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, TextArea

##############################################################################
# Local imports.
from ...peps import API
from ..data import PEP, cache_dir
from ..widgets import TextViewer


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
            border: solid $border;
        }

        TextViewer {
            color: $text-muted;
            height: 1fr;
            scrollbar-background: $panel;
            scrollbar-background-hover: $panel;
            scrollbar-background-active: $panel;
            &:focus {
                color: $text;
            }
        }

        #buttons {
            height: auto;
            align-horizontal: right;
            border-top: solid $border;
        }

        Button {
            margin-right: 1;
        }
    }
    """

    BINDINGS = [("escape", "close"), ("ctrl+r", "refresh"), ("ctrl+c", "copy")]

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
            yield TextViewer()
            with Horizontal(id="buttons"):
                yield Button("Copy [dim]\\[^c][/]", id="copy")
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
        (text := self.query_one(TextViewer)).loading = True
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

        text.text = pep_source
        text.loading = False
        self.set_focus(text)

    def on_mount(self) -> None:
        """Populate the dialog once the DOM is ready."""
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

    @on(Button.Pressed, "#copy")
    async def action_copy(self) -> None:
        """Copy PEP text to the clipboard."""
        await self.query_one(TextArea).run_action("copy")


### pep_viewer.py ends here
