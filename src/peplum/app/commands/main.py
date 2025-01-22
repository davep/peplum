"""The main commands used within the application."""

##############################################################################
# Local imports.
from .base import Command


##############################################################################
class ChangeTheme(Command):
    """Change the application's theme"""

    BINDING_KEY = "f9"
    SHOW_IN_FOOTER = False


##############################################################################
class Escape(Command):
    "Back up through the panes, right to left, or exit the app if the navigation pane has focus"

    BINDING_KEY = "escape"
    SHOW_IN_FOOTER = False


##############################################################################
class Help(Command):
    """Show help for and information about the application"""

    BINDING_KEY = "f1, ?"


##############################################################################
class Quit(Command):
    """Quit the application"""

    BINDING_KEY = "f10, ctrl+q"


##############################################################################
class RedownloadPEPs(Command):
    """Redownload the list of PEPs"""

    FOOTER_TEXT = "Redownload"
    COMMAND = "Redownload all PEPs"
    BINDING_KEY = "ctrl+r"
    ACTION = "redownload_peps_command"


##############################################################################
class TogglePEPDetails(Command):
    """Toggle the display of the PEP details panel"""

    FOOTER_TEXT = "Details"
    COMMAND = "Toggle PEP details"
    BINDING_KEY = "f3"
    ACTION = "toggle_pep_details_command"


### main.py ends here
