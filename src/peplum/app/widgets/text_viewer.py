"""A widget for viewing text."""

##############################################################################
# Textual imports.
from textual.widgets import TextArea


##############################################################################
class TextViewer(TextArea):
    """A widget for viewing text."""

    DEFAULT_CSS = """
    TextViewer {
        background: transparent;
        border: none;
        &:focus {
            border: none;
        }
        & > .text-area--cursor-line {
           background: transparent;
        }
    }
    """

    BINDINGS = [
        ("<", "cursor_line_start"),
        (">", "cursor_line_end"),
        ("c, C", "copy"),
    ]

    def __init__(
        self,
        text: str = "",
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialise the object.

        Args:
            text: The text to view.
            name: The name of the TextViewer.
            id: The ID of the TextViewer in the DOM.
            classes: The CSS classes of the TextViewer.
            disabled: Whether the TextViewer is disabled or not.
        """
        super().__init__(
            text,
            read_only=True,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def action_copy(self) -> None:
        """Action for copying text to the clipboard."""
        if for_clipboard := self.selected_text:
            self.notify("Selected text copied to the clipboard.")
        else:
            for_clipboard = self.text
            self.notify("All text copied to the clipboard.")
        self.app.copy_to_clipboard(for_clipboard)

    def action_cursor_line_start(self, select: bool = False) -> None:
        """Add a slightly smarter use of going 'home'."""
        if self.cursor_at_start_of_line:
            self.move_cursor(self.document.start, select=select)
        else:
            super().action_cursor_line_start(select)

    def action_cursor_line_end(self, select: bool = False) -> None:
        """Add a slightly smarter use of going 'end'."""
        if self.cursor_at_end_of_line:
            self.move_cursor(self.document.end, select=select)
        else:
            super().action_cursor_line_end(select)


### text_viewer.py ends here
