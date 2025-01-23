"""Provides functions and classes for managing the app's data."""

##############################################################################
# Local imports.
from .config import (
    Configuration,
    load_configuration,
    save_configuration,
    update_configuration,
)
from .peps import (
    AuthorCount,
    Containing,
    PEPCount,
    PEPs,
    PythonVersionCount,
    StatusCount,
    TypeCount,
    WithAuthor,
    WithPythonVersion,
    WithStatus,
    WithType,
    pep_data,
)

##############################################################################
# Exports.
__all__ = [
    "pep_data",
    "AuthorCount",
    "Configuration",
    "Containing",
    "load_configuration",
    "PEPCount",
    "PEPs",
    "PythonVersionCount",
    "save_configuration",
    "StatusCount",
    "TypeCount",
    "update_configuration",
    "WithAuthor",
    "WithPythonVersion",
    "WithStatus",
    "WithType",
]

### __init__.py ends here
