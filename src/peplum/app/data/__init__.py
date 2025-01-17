"""Provides functions and classes for managing the app's data."""

##############################################################################
# Local imports.
from .config import load_configuration, save_configuration, update_configuration
from .peps import (
    AuthorCount,
    PEPs,
    PythonVersionCount,
    StatusCount,
    TypeCount,
    WithAuthor,
    WithPythonVersion,
    WithStatus,
    WithType,
)

##############################################################################
# Exports.
__all__ = [
    "load_configuration",
    "save_configuration",
    "update_configuration",
    "AuthorCount",
    "PEPs",
    "PythonVersionCount",
    "StatusCount",
    "TypeCount",
    "WithAuthor",
    "WithPythonVersion",
    "WithStatus",
    "WithType",
]

### __init__.py ends here
