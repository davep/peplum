"""Python version filtering commands for the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import CommandHit, CommandHits, CommandsProvider

##############################################################################
# Local imports.
from ..data import PEPs
from ..messages import ShowPythonVersion


##############################################################################
class PythonVersionCommands(CommandsProvider):
    """A command palette provider related to Python versions."""

    active_peps: PEPs | None = None
    """The currently-active collection of PEPs to get the Python versions of."""

    @classmethod
    def prompt(cls) -> str:
        """The prompt for the command provider."""
        return (
            "Also search for PEPs related to Python version..."
            if cls.active_peps and cls.active_peps.is_filtered
            else "Search for PEPs related to Python version..."
        )

    def commands(self) -> CommandHits:
        """Provide the Python version-based command data for the command palette.

        Yields:
            The commands for the command palette.
        """
        if self.active_peps is None:
            return
        help_prefix, command_prefix = (
            ("Also filter", "Filter")
            if self.active_peps.is_filtered
            else ("Also relating to Python version", "Relating to Python version")
        )
        for version in sorted(self.active_peps.python_versions):
            if not version.version:
                yield CommandHit(
                    "Also isn't related to a specific Python version"
                    if self.active_peps.is_filtered
                    else "Isn't related to a specific Python version",
                    f"{help_prefix} to PEPs unrelated to any specific Python version (narrows down to {version.count})",
                    ShowPythonVersion(""),
                )
            else:
                yield CommandHit(
                    f"{command_prefix} {version.version}",
                    f"{help_prefix} to PEPs related to Python version {version.version} (narrows down to {version.count})",
                    ShowPythonVersion(version.version),
                )


### python_versions.py ends here
