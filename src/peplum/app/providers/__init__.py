"""Provides the command palette command provides for the application."""

##############################################################################
# Local imports.
from .authors import AuthorCommands
from .commands_provider import CommandsProvider
from .main import MainCommands
from .peps import PEPsCommands
from .python_versions import PythonVersionCommands
from .statuses import StatusCommands
from .types import TypeCommands

##############################################################################
# Exports.
__all__ = [
    "AuthorCommands",
    "CommandsProvider",
    "MainCommands",
    "PEPsCommands",
    "PythonVersionCommands",
    "StatusCommands",
    "TypeCommands",
]

### __init__.py ends here
