"""Provides functions and classes for managing the app's data."""

##############################################################################
# Local imports.
from .config import load_configuration, save_configuration, update_configuration
from .peps import PEPs, StatusCount, TypeCount

##############################################################################
# Exports.
__all__ = [
    "load_configuration",
    "save_configuration",
    "update_configuration",
    "PEPs",
    "StatusCount",
    "TypeCount",
]

### __init__.py ends here
