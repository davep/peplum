"""The main navigation panel."""

##############################################################################
# Rich imports.
from rich.console import Group, RenderableType
from rich.rule import Rule
from rich.table import Table

##############################################################################
# Textual imports.
from textual.reactive import var
from textual.widgets.option_list import Option

##############################################################################
# Typing exception imports.
from typing_extensions import Self

##############################################################################
# Local imports.
from ..data import PEPs, PythonVersionCount, StatusCount, TypeCount
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
class CountView(Option):
    """Base class for options that show a count."""

    def count_prompt(self, caption: str, count: int) -> RenderableType:
        """Create a prompt.

        Args:
            caption: The caption for the prompt.
            count: The count for the prompt.

        Returns:
            The prompt.
        """
        prompt = Table.grid(expand=True)
        prompt.add_column(ratio=1)
        prompt.add_column(justify="right")
        prompt.add_row(caption, f"[dim i]{count}[/]")
        return prompt


##############################################################################
class AllView(CountView):
    """Option used to signify that we should view all PEPs."""

    def __init__(self, peps: PEPs) -> None:
        """Initialise the object.

        Args:
            peps: The full collection of PEPs.
        """
        super().__init__(self.count_prompt("All", len(peps)), id=f"_all_peps")


##############################################################################
class TypeView(CountView):
    """Option for showing a PEP type."""

    def __init__(self, pep_type: TypeCount) -> None:
        """Initialise the object.

        Args:
            pep_type: The details of the PEP type to show.
        """
        self._type = pep_type
        """The details of the type to show."""
        super().__init__(
            self.count_prompt(pep_type.type, pep_type.count),
            id=f"_type_{pep_type.type}",
        )


##############################################################################
class StatusView(CountView):
    """Option for showing a PEP status."""

    def __init__(self, status: StatusCount) -> None:
        """ "Initialise the object.

        Args:
            status: The details of the PEP status to show.
        """
        self._status = status
        """The details of the status to show."""
        super().__init__(
            self.count_prompt(status.status, status.count),
            id=f"_status_{status.status}",
        )


##############################################################################
class PythonVersionView(CountView):
    """Option for showing a Python version."""

    def __init__(self, version: PythonVersionCount) -> None:
        """ "Initialise the object.

        Args:
            version: The details of the PEP Python version to show.
        """
        super().__init__(
            self.count_prompt(version.version or f"[dim i]None[/]", version.count),
            id=f"_python_version_{version.version}",
        )


##############################################################################
class Navigation(OptionListEx):
    """The main navigation panel."""

    all_peps: var[PEPs] = var(PEPs)
    """The collection of all known PEPs."""

    active_peps: var[PEPs] = var(PEPs)
    """The currently-active collection of PEPs."""

    def add_main(self) -> Self:
        """Add the main navigation options.

        Returns:
            Self.
        """
        return self.add_option(AllView(self.all_peps))

    def add_types(self) -> Self:
        """Add the PEP types to navigation.

        Returns:
            Self.
        """
        if self.active_peps:
            self.add_option(Title("Type"))
            for pep_type in sorted(self.active_peps.types):
                self.add_option(TypeView(pep_type))
        return self

    def add_statuses(self) -> Self:
        """Add the PEP statuses to navigation.

        Returns:
            Self.
        """
        if self.active_peps:
            self.add_option(Title(f"Status"))
            for status in sorted(self.active_peps.statuses):
                self.add_option(StatusView(status))
        return self

    def add_python_versions(self) -> Self:
        """Add the PEP python versions to navigation.

        Returns:
            Self.
        """
        if self.active_peps:
            self.add_option(Title("Python Versions"))
            for version in sorted(self.active_peps.python_versions):
                self.add_option(PythonVersionView(version))
        return self

    def repopulate(self) -> None:
        """Repopulate navigation panel."""
        with self.preserved_highlight:
            self.clear_options().add_main().add_types().add_statuses().add_python_versions()
        if self.highlighted is None:
            self.highlighted = 0

    def watch_all_peps(self) -> None:
        """React to the full list of PEPs being changed."""
        self.repopulate()

    def watch_active_peps(self) -> None:
        """React to the active PEPs being changed."""
        self.repopulate()


### navigation.py ends here
