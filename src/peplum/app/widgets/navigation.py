"""The main navigation panel."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import Callable

##############################################################################
# Rich imports.
from rich.console import Group, RenderableType
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
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Typing exception imports.
from typing_extensions import Self

##############################################################################
# Local imports.
from ..commands import ShowAll
from ..data import (
    AuthorCount,
    Configuration,
    PEPCount,
    PEPs,
    PythonVersionCount,
    StatusCount,
    TypeCount,
)
from ..messages import ShowAuthor, ShowPythonVersion, ShowStatus, ShowType


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

    @property
    def command(self) -> Message:
        """The command to send when this option is selected."""
        raise NotImplementedError


##############################################################################
class AllView(CountView):
    """Option used to signify that we should view all PEPs."""

    def __init__(self, peps: PEPs, key: str, key_colour: str | None) -> None:
        """Initialise the object.

        Args:
            peps: The full collection of PEPs.
        """
        super().__init__(
            self.count_prompt(f"All [{(key_colour or 'dim')}]\\[{key}][/]", len(peps)),
            id=f"_all_peps",
        )

    @property
    def command(self) -> Message:
        """The command to send when this option is selected."""
        return ShowAll()


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

    @property
    def command(self) -> Message:
        """The command to send when this option is selected."""
        return ShowType(self._type.type)


##############################################################################
class StatusView(CountView):
    """Option for showing a PEP status."""

    def __init__(self, status: StatusCount) -> None:
        """Initialise the object.

        Args:
            status: The details of the PEP status to show.
        """
        self._status = status
        """The details of the status to show."""
        super().__init__(
            self.count_prompt(status.status, status.count),
            id=f"_status_{status.status}",
        )

    @property
    def command(self) -> Message:
        """The command to send when this option is selected."""
        return ShowStatus(self._status.status)


##############################################################################
class PythonVersionView(CountView):
    """Option for showing a Python version."""

    def __init__(self, version: PythonVersionCount) -> None:
        """Initialise the object.

        Args:
            version: The details of the PEP Python version to show.
        """
        self._version = version
        """The Python version to show."""
        super().__init__(
            self.count_prompt(version.version or f"[dim i]None[/]", version.count),
            id=f"_python_version_{version.version}",
        )

    @property
    def command(self) -> Message:
        """The command to send when this option is selected."""
        return ShowPythonVersion(self._version.version)


##############################################################################
class AuthorView(CountView):
    """Option for showing a PEP author."""

    def __init__(self, author: AuthorCount) -> None:
        """Initialise the object.

        Args:
            author: The details of the PEP author to show.
        """
        self._author = author
        """The details of the author to show."""
        super().__init__(
            self.count_prompt(author.author, author.count),
            id=f"_author_{author.author}",
        )

    @property
    def command(self) -> Message:
        """The command to send when this option is selected."""
        return ShowAuthor(self._author.author)


##############################################################################
class Navigation(EnhancedOptionList):
    """The main navigation panel."""

    HELP = """
    ## Navigation Panel

    Select items in this panel to filter the list of PEPs.
    """

    all_peps: var[PEPs] = var(PEPs)
    """The collection of all known PEPs."""

    active_peps: var[PEPs] = var(PEPs)
    """The currently-active collection of PEPs."""

    sort_types_by_count: var[bool] = var(True)
    """Sort the types by their count?"""

    sort_statuses_by_count: var[bool] = var(True)
    """Sort the statuses by their count?"""

    sort_python_versions_by_count: var[bool] = var(True)
    """Sort the Python versions by their count?"""

    sort_authors_by_count: var[bool] = var(True)
    """Sort the authors by their count?"""

    def __init__(
        self, config: Configuration, id: str | None = None, classes: str | None = None
    ):
        """Initialise the widget.

        Args:
            config: THe configuration for the application.
            id: The ID for the widget.
            classes: The classes for the widget.
        """
        super().__init__(id=id, classes=classes)
        self.set_reactive(Navigation.sort_types_by_count, config.sort_types_by_count)
        self.set_reactive(
            Navigation.sort_statuses_by_count, config.sort_statuses_by_count
        )
        self.set_reactive(
            Navigation.sort_python_versions_by_count,
            config.sort_python_versions_by_count,
        )
        self.set_reactive(
            Navigation.sort_authors_by_count, config.sort_authors_by_count
        )

    def on_mount(self) -> None:
        """Configure the widget once the DOM is mounted."""
        self.app.theme_changed_signal.subscribe(self, lambda _: self.repopulate())

    def add_main(self) -> Self:
        """Add the main navigation options.

        Returns:
            Self.
        """
        return self.add_option(
            AllView(
                self.all_peps,
                key=ShowAll.key_binding(),
                key_colour=None
                if self.app.current_theme is None
                else self.app.current_theme.accent,
            )
        )

    @staticmethod
    def _filter_key(by_count: bool) -> Callable[[PEPCount], int | PEPCount]:
        """Get a key for sorting a filter in navigation.

        Args:
            by_count: Should we sort by count?

        Returns:
            A function to get the correct key to sort on.
        """

        def _key(count: PEPCount) -> int | PEPCount:
            return -count.count if by_count else count

        return _key

    def add_types(self) -> Self:
        """Add the PEP types to navigation.

        Returns:
            Self.
        """
        if self.active_peps:
            self.add_option(Title("Type"))
            for pep_type in sorted(
                self.active_peps.types, key=self._filter_key(self.sort_types_by_count)
            ):
                self.add_option(TypeView(pep_type))
        return self

    def add_statuses(self) -> Self:
        """Add the PEP statuses to navigation.

        Returns:
            Self.
        """
        if self.active_peps:
            self.add_option(Title("Status"))
            for status in sorted(
                self.active_peps.statuses,
                key=self._filter_key(self.sort_statuses_by_count),
            ):
                self.add_option(StatusView(status))
        return self

    def add_python_versions(self) -> Self:
        """Add the PEP python versions to navigation.

        Returns:
            Self.
        """
        if self.active_peps:
            self.add_option(Title("Python Version"))
            for version in sorted(
                self.active_peps.python_versions,
                key=self._filter_key(self.sort_python_versions_by_count),
            ):
                self.add_option(PythonVersionView(version))
        return self

    def add_authors(self) -> Self:
        """Add the PEP authors to navigation.

        Returns:
            Self.
        """
        if self.active_peps:
            self.add_option(Title("Author"))
            for author in sorted(
                self.active_peps.authors,
                key=self._filter_key(self.sort_authors_by_count),
            ):
                self.add_option(AuthorView(author))
        return self

    def repopulate(self) -> None:
        """Repopulate navigation panel."""
        with self.preserved_highlight:
            self.clear_options().add_main().add_types().add_statuses().add_python_versions().add_authors()

    def watch_all_peps(self) -> None:
        """React to the full list of PEPs being changed."""
        self.repopulate()

    def watch_active_peps(self) -> None:
        """React to the active PEPs being changed."""
        self.repopulate()

    def watch_sort_types_by_count(self) -> None:
        """React to the types sort order being changed."""
        self.repopulate()

    def watch_sort_statuses_by_count(self) -> None:
        """React to the statuses sort order being changed."""
        self.repopulate()

    def watch_sort_python_versions_by_count(self) -> None:
        """React to the Python versions sort order being changed."""
        self.repopulate()

    def watch_sort_authors_by_count(self) -> None:
        """React to the authors sort order being changed."""
        self.repopulate()

    @on(OptionList.OptionSelected)
    def navigate(self, event: OptionList.OptionSelected) -> None:
        event.stop()
        assert isinstance(event.option, CountView)
        self.post_message(event.option.command)


### navigation.py ends here
