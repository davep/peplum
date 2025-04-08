"""Provides functions and classes for managing the app's data."""

##############################################################################
# Local imports.
from .config import (
    Configuration,
    load_configuration,
    save_configuration,
    update_configuration,
)
from .locations import cache_dir
from .notes import Notes
from .pep import PEP, PEPStatus, PEPType, PostHistory
from .peps import (
    AuthorCount,
    Containing,
    PEPCount,
    PEPs,
    PythonVersionCount,
    SortOrder,
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
    "AuthorCount",
    "cache_dir",
    "Configuration",
    "Containing",
    "load_configuration",
    "Notes",
    "PEP",
    "pep_data",
    "PEPCount",
    "PEPs",
    "PEPStatus",
    "PEPType",
    "PostHistory",
    "PythonVersionCount",
    "save_configuration",
    "SortOrder",
    "StatusCount",
    "TypeCount",
    "update_configuration",
    "WithAuthor",
    "WithPythonVersion",
    "WithStatus",
    "WithType",
]

### __init__.py ends here
