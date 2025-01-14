"""Provides the main application class."""

##############################################################################
# Textual imports.
from textual.app import App
from textual.binding import Binding

##############################################################################
# Local imports.
from .screens import Main


##############################################################################
class Peplum(App[None]):
    """The main application class."""

    CSS = """
    CommandPalette > Vertical {
        width: 75%; /* Full-width command palette looks like garbage. Fix that. */
        background: $panel;
        SearchIcon {
            display: none;
        }
        OptionList {
            /* Make the scrollbar less gross. */
            scrollbar-background: $panel;
            scrollbar-background-hover: $panel;
            scrollbar-background-active: $panel;
        }
    }

    /* Remove cruft from the Header. */
    Header {
        /* The header icon is ugly and pointless. Remove it. */
        HeaderIcon {
            visibility: hidden;
        }

        /* The tall version of the header is utterly useless. Nuke that. */
        &.-tall {
            height: 1 !important;
        }
    }

    /* General style tweaks that affect all widgets. */
    * {
        /* Let's make scrollbars a wee bit thinner. */
        scrollbar-size-vertical: 1;
    }
    """

    BINDINGS = [
        Binding(
            "ctrl+p, super+x, :",
            "command_palette",
            "Commands",
            show=False,
            tooltip="Show the command palette",
        ),
    ]

    def on_mount(self) -> None:
        """Display the main screen."""
        self.push_screen(Main())


### peplum.py ends here
