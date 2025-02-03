"""Commands for locating and jumping to a PEP."""

##############################################################################
# Python imports.
from operator import attrgetter

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import CommandHit, CommandHits, CommandsProvider

##############################################################################
# Local imports.
from ..data import PEPs
from ..messages import GotoPEP


##############################################################################
class PEPsCommands(CommandsProvider):
    """A command palette provider for finding and jumping to a PEP."""

    peps: PEPs | None = None
    """The list of PEPs to show."""

    @classmethod
    def prompt(cls) -> str:
        """The prompt for the command provider."""
        return "Jump to PEP..."

    def commands(self) -> CommandHits:
        """Provide a list of commands for jumping to a specific PEP.

        Yields:
           Commands to show in the command palette.
        """
        if self.peps is None:
            return
        for pep in sorted(self.peps, key=attrgetter("number")):
            yield CommandHit(f"Jump to PEP{pep.number}", pep.title, GotoPEP(pep.number))


### peps.py ends here
