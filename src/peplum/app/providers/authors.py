"""Author filtering commands for the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import CommandHit, CommandHits, CommandsProvider

##############################################################################
# Local imports.
from ..data import PEPs
from ..messages import ShowAuthor


##############################################################################
class AuthorCommands(CommandsProvider):
    """A command palette provider related to authors."""

    active_peps: PEPs | None = None
    """The currently-active collection of PEPs to get the authors of."""

    @classmethod
    def prompt(cls) -> str:
        """The prompt for the command provider."""
        return (
            "Also search for PEPs authored by..."
            if cls.active_peps and cls.active_peps.is_filtered
            else "Search for PEPs authored by..."
        )

    def commands(self) -> CommandHits:
        """Provide the author-based command data for the command palette.

        Yields:
            The commands for the command palette.
        """
        if self.active_peps is None:
            return
        help_prefix, command_prefix = (
            ("Also filter", "Also authored by")
            if self.active_peps.is_filtered
            else ("Filter", "Authored by")
        )
        for author in self.active_peps.authors:
            yield CommandHit(
                f"{command_prefix} {author.author}",
                f"{help_prefix} to PEPs authored by {author.author} (narrows down to {author.count})",
                ShowAuthor(author.author),
            )


### authors.py ends here
