"""The main navigation panel."""

##############################################################################
# Rich imports.
from rich.console import Group
from rich.rule import Rule

##############################################################################
# Textual imports.
from textual.reactive import var
from textual.widgets.option_list import Option

##############################################################################
# Typing exception imports.
from typing_extensions import Self

##############################################################################
# Local imports.
from ..data import PEPs
from .extended_option_list import OptionListEx


##############################################################################
class Title(Option):
    """Option for showing a title."""

    def __init__(self, title: str) -> None:
        """Initialise the object.

        Args:
            title: The title to show.
        """
        super().__init__(
            Group("", Rule(title, style="bold dim")),
            disabled=True,
            id=f"_title_{title}",
        )


##############################################################################
class Navigation(OptionListEx):
    """The main navigation panel."""

    peps: var[PEPs] = var(PEPs, always_update=True)
    """The currently-active collection of PEPs."""

    def add_main(self) -> Self:
        """Add the main navigation options.

        Returns:
            Self.
        """
        return self.add_option(f"All ({len(self.peps)})")

    def add_types(self) -> Self:
        """Add the PEP types to navigation.

        Returns:
            Self.
        """
        self.add_option(Title("Type"))
        for pep_type in sorted(self.peps.types):
            self.add_option(f"{pep_type.type} ({pep_type.count})")
        return self

    def add_statuses(self) -> Self:
        """Add the PEP statuses to navigation.

        Returns:
            Self.
        """
        self.add_option(Title("Status"))
        for status in sorted(self.peps.statuses):
            self.add_option(f"{status.status} ({status.count})")
        return self

    def watch_peps(self) -> None:
        """React to the PEPs being changed."""
        with self.preserved_highlight:
            self.clear_options().add_main().add_types().add_statuses()
        if self.highlighted is None:
            self.highlighted = 0


### navigation.py ends here
