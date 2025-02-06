"""PEP status filtering commands for the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import CommandHit, CommandHits, CommandsProvider

##############################################################################
# Local imports.
from ..data import PEPs
from ..messages import ShowStatus


##############################################################################
class StatusCommands(CommandsProvider):
    """A command palette provider related to statuses."""

    active_peps: PEPs | None = None
    """The currently-active collection of PEPs to get the statuses of."""

    @classmethod
    def prompt(cls) -> str:
        """The prompt for the command provider."""
        return (
            "Also search for PEPs of with status..."
            if cls.active_peps and cls.active_peps.is_filtered
            else "Search for PEPs with status..."
        )

    def commands(self) -> CommandHits:
        """Provide the status-based command data for the command palette.

        Yields:
            The commands for the command palette.
        """
        if self.active_peps is None:
            return
        help_prefix, command_prefix = (
            ("Also filter", "Filter")
            if self.active_peps.is_filtered
            else ("Also with status", "With status")
        )
        for status in self.active_peps.statuses:
            yield CommandHit(
                f"{command_prefix} {status.status}",
                f"{help_prefix} to PEPs with status {status.status} (narrows down to {status.count})",
                ShowStatus(status.status),
            )


### statuses.py ends here
