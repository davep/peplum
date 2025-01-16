"""Provides a class for letting the user view a list of PEPs."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# Rich imports.
from rich.console import Group
from rich.markup import escape
from rich.rule import Rule
from rich.table import Table

##############################################################################
# Textual imports.
from textual.reactive import var
from textual.widgets.option_list import Option

##############################################################################
# Local imports.
from ...peps import PEP
from ..data import PEPs
from .extended_option_list import OptionListEx


##############################################################################
class PEPView(Option):
    """Option for viewing a single PEP."""

    RULE: Final[Rule] = Rule(style="dim")
    """The rule to place at the end of each view."""

    def __init__(self, pep: PEP) -> None:
        """Initialise the object.

        Args:
            pep: The PEP to view.
        """

        title = Table.grid(expand=True)
        title.add_column(width=6)
        title.add_column(justify="left", ratio=2)
        title.add_column(justify="right", width=28)
        title.add_row(
            f"{pep.number}", escape(pep.title), f"[dim]{pep.type}, {pep.status}[/]"
        )

        info = Table.grid(expand=True)
        info.add_column(width=6)
        info.add_column(ratio=1)
        info.add_column(width=11, justify="right")
        info.add_row("", f"[dim]{', '.join(pep.authors)}[/]", f"[dim]{pep.created}[/]")

        super().__init__(Group(title, info, self.RULE), id=f"PEP{pep.number}")


##############################################################################
class PEPsView(OptionListEx):
    """A widget for viewing a list of PEPs."""

    active_peps: var[PEPs] = var(PEPs, always_update=True)
    """The currently-active collection of PEPs."""

    async def watch_active_peps(self) -> None:
        """React to the PEPs being changed."""
        with self.preserved_highlight:
            self.clear_options().add_options(PEPView(pep) for pep in self.active_peps)


### peps_view.py ends here
