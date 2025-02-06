"""PEP type filtering commands for the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import CommandHit, CommandHits, CommandsProvider

##############################################################################
# Local imports.
from ..data import PEPs
from ..messages import ShowType


##############################################################################
class TypeCommands(CommandsProvider):
    """A command palette provider related to types."""

    active_peps: PEPs | None = None
    """The currently-active collection of PEPs to get the types of."""

    @classmethod
    def prompt(cls) -> str:
        """The prompt for the command provider."""
        return (
            "Also search for PEPs of type..."
            if cls.active_peps and cls.active_peps.is_filtered
            else "Search for PEPs of type..."
        )

    def commands(self) -> CommandHits:
        """Provide the type-based command data for the command palette.

        Yields:
            The commands for the command palette.
        """
        if self.active_peps is None:
            return
        help_prefix, command_prefix = (
            ("Also filter", "Filter")
            if self.active_peps.is_filtered
            else ("Also of type", "Of type")
        )
        for pep_type in self.active_peps.types:
            yield CommandHit(
                f"{command_prefix} {pep_type.type}",
                f"{help_prefix} to PEPs of type {pep_type.type} (narrows down to {pep_type.count})",
                ShowType(pep_type.type),
            )


### types.py ends here
