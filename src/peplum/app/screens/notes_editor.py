"""A dialog for editing a PEP's notes."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, TextArea

##############################################################################
# Local imports.
from ..data import PEP


##############################################################################
class NotesEditor(ModalScreen[str | None]):
    """A modal screen for editing some notes."""

    CSS = """
    NotesEditor {
        align: center middle;

        &> Vertical {
            width: 60%;
            max-width: 80;
            height: auto;
            background: $panel;
            border: panel $border;
        }

        TextArea, TextArea:focus {
            height: 20;
            margin: 1 1 0 1;
            padding: 0;
            border: none;
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

    BINDINGS = [("escape", "cancel"), ("f2", "save")]

    def __init__(self, pep: PEP) -> None:
        """Initialise the dialog.

        Args:
            pep: The PEP to edit the notes for.
        """
        super().__init__()
        self._pep = pep
        """The PEP whose notes are being edited."""

    def compose(self) -> ComposeResult:
        """Compose the dialog's content."""
        with Vertical() as dialog:
            dialog.border_title = f"Notes for PEP{self._pep.number}"
            yield TextArea(self._pep.notes)
            with Horizontal(id="buttons"):
                yield Button("Save [dim]\\[F2][/]", id="save", variant="success")
                yield Button("Cancel [dim]\\[Esc][/]", id="cancel", variant="error")

    @on(Button.Pressed, "#save")
    def action_save(self) -> None:
        """Save the notes."""
        self.dismiss(self.query_one(TextArea).text)

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel the edit of the notes."""
        self.dismiss(None)


### notes_editor.py ends here
