"""Provides a class for letting the user view a list of PEPs."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from typing import Final

##############################################################################
# Rich imports.
from rich.console import Group
from rich.markup import escape
from rich.rule import Rule
from rich.table import Table

##############################################################################
# Textual imports.
from textual import on
from textual.message import Message
from textual.reactive import var
from textual.widgets import OptionList
from textual.widgets.option_list import Option

##############################################################################
# Local imports.
from ...peps import PEP
from ..data import PEPs
from ..messages import VisitPEP
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
            f"[bold]{pep.number}[/]",
            escape(pep.title),
            f"[dim]{pep.type}, {pep.status}[/]",
        )

        info = Table.grid(expand=True)
        info.add_column(width=6)
        info.add_column(ratio=1)
        info.add_column(width=11, justify="right")
        info.add_row("", f"[dim]{', '.join(pep.authors)}[/]", f"[dim]{pep.created}[/]")

        self._pep = pep
        """The PEP that this option is showing."""

        super().__init__(Group(title, info, self.RULE), id=f"PEP{pep.number}")

    @property
    def pep(self) -> PEP:
        """The PEP associated with this option."""
        return self._pep


##############################################################################
class PEPsView(OptionListEx):
    """A widget for viewing a list of PEPs."""

    HELP = """
    ## The PEPs List

    This is a list of all PEPs that match your current filter.
    """

    active_peps: var[PEPs] = var(PEPs)
    """The currently-active collection of PEPs."""

    def watch_active_peps(self) -> None:
        """React to the PEPs being changed."""
        with self.preserved_highlight:
            self.clear_options().add_options(PEPView(pep) for pep in self.active_peps)

    @dataclass
    class PEPHighlighted(Message):
        """A message that is posted when a PEP is highlighted by the user."""

        pep: PEP
        """The highlighted PEP."""

    @on(OptionList.OptionHighlighted)
    def select_pep(self, message: OptionList.OptionSelected) -> None:
        """Send a message to say a particular PEP has been selected."""
        message.stop()
        assert isinstance(message.option, PEPView)
        self.post_message(self.PEPHighlighted(message.option.pep))

    @on(OptionList.OptionSelected)
    def visit_pep(self, message: OptionList.OptionSelected) -> None:
        """Send a message to say the user wants to visit a PEP's webpage."""
        message.stop()
        assert isinstance(message.option, PEPView)
        self.post_message(VisitPEP(message.option.pep))


### peps_view.py ends here
