"""The main commands used within the application."""

##############################################################################
# Local imports.
from .base import Command


##############################################################################
class ChangeTheme(Command):
    """Change the application's theme"""

    BINDING_KEY = "f9"


##############################################################################
class EditNotes(Command):
    """Edit the highlighted PEP's notes"""

    BINDING_KEY = "f2"
    FOOTER_TEXT = "Notes"
    SHOW_IN_FOOTER = True


##############################################################################
class Escape(Command):
    "Back up through the panes, right to left, or exit the app if the navigation pane has focus"

    BINDING_KEY = "escape"


##############################################################################
class Help(Command):
    """Show help for and information about the application"""

    BINDING_KEY = "f1, ?"
    SHOW_IN_FOOTER = True


##############################################################################
class Quit(Command):
    """Quit the application"""

    BINDING_KEY = "f10, ctrl+q"
    SHOW_IN_FOOTER = True


##############################################################################
class RedownloadPEPs(Command):
    """Redownload the list of PEPs"""

    FOOTER_TEXT = "Redownload"
    COMMAND = "Redownload All PEPs"
    BINDING_KEY = "ctrl+r"
    ACTION = "redownload_peps_command"
    SHOW_IN_FOOTER = True


##############################################################################
class TogglePEPDetails(Command):
    """Toggle the display of the PEP details panel"""

    FOOTER_TEXT = "Details"
    BINDING_KEY = "f3"
    SHOW_IN_FOOTER = True


##############################################################################
class ViewPEP(Command):
    """View the source of the currently-highlighted PEP"""

    FOOTER_TEXT = "View"
    BINDING_KEY = "f4"
    SHOW_IN_FOOTER = True


### main.py ends here
