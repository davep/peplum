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
    }
    """

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


### text_viewer.py ends here
