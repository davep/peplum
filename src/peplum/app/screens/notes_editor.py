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
            border: solid $border;
        }

        TextArea, TextArea:focus {
            background: transparent;
            height: 20;
            padding: 0;
            border: none;
            scrollbar-background: $panel;
            scrollbar-background-hover: $panel;
            scrollbar-background-active: $panel;
            & > .text-area--cursor-line {
               background: transparent;
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
        key_colour = (
            "dim" if self.app.current_theme is None else self.app.current_theme.accent
        )
        with Vertical() as dialog:
            dialog.border_title = f"Notes for PEP{self._pep.number}"
            yield TextArea(self._pep.notes)
            with Horizontal(id="buttons"):
                yield Button(f"Save [{key_colour}]\\[F2][/]", id="save")
                yield Button(f"Cancel [{key_colour}]\\[Esc][/]", id="cancel")

    @on(Button.Pressed, "#save")
    def action_save(self) -> None:
        """Save the notes."""
        self.dismiss(self.query_one(TextArea).text)

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel the edit of the notes."""
        self.dismiss(None)


### notes_editor.py ends here
