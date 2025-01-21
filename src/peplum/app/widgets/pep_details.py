"""Provides a widget for showing a PEP's details."""

##############################################################################
# Python imports.
from datetime import date, datetime
from functools import singledispatchmethod
from typing import Sequence

##############################################################################
# Humanize imports
from humanize import naturaltime

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.events import DescendantBlur, DescendantFocus
from textual.reactive import var
from textual.widgets import Label

##############################################################################
# Local imports.
from ...peps import PEP
from .extended_option_list import OptionListEx


##############################################################################
def date_display(display_date: date) -> str:
    """Format a date for display.

    Args:
        display_date: The date to format for display.

    Returns:
        The date formatted for display.
    """
    return f"{display_date} ({naturaltime(datetime.combine(display_date, datetime.min.time()))})"


##############################################################################
class Field(Vertical):
    """A container class that gives a widget a title."""

    DEFAULT_CSS = """
    Field {
        height: auto;
        margin-bottom: 1;
        &.hidden {
            display: none;
        }

        & > #_field_title {
            color: $text-accent;
            width: 1fr;
            background: $boost;
        }
    }
    """

    def __init__(self, title: str) -> None:
        """Initialise the widget.

        Args:
            title: The title to give the widget.
        """
        super().__init__(classes="hidden")
        self.compose_add_child(Label(title, id="_field_title"))


##############################################################################
class Value(Label):
    """A label that will hide itself if empty or `None`."""

    def show(self, text: str | int | None) -> None:
        """Show the given text, or possibly hide.

        Args:
            text: The text to show, or `None`.
        """
        if self.parent is None:
            return
        if isinstance(text, int):
            text = str(text)
        self.parent.set_class(not bool(text), "hidden")
        if text:
            self.update(text)


##############################################################################
class List(OptionListEx):
    """Show a list of values that the user can pick from."""

    DEFAULT_CSS = """
    List, List:focus {
        height: auto;
        width: auto;
        border: none;
        background: transparent !important;
        margin: 0;
        padding: 0;
        /* Stop a flash of unnecessary scrollbar. */
        scrollbar-size-vertical: 0;
        overflow-y: hidden;
    }
    """

    @singledispatchmethod
    def show(self, values: Sequence[str | int | None]) -> None:
        """Show the list.

        Args:
            values: The values to show.
        """
        if self.parent is None:
            return
        self.parent.set_class(not bool(values), "hidden")
        self.clear_options().add_options([str(value) for value in values])

    @show.register
    def _(self, values: str | int | None) -> None:
        if values is not None:
            self.show([values])

    def on_focus(self) -> None:
        """Ensure the highlight appears when we get focus."""
        if self.highlighted is None and self.option_count:
            self.highlighted = 0

    def on_blur(self) -> None:
        """Remove the highlight when we no longer have focus."""
        self.highlighted = None


##############################################################################
class PEPDetails(VerticalScroll):
    """A widget for showing details of a PEP."""

    pep: var[PEP | None] = var(None)
    """The PEP to show the details of."""

    def compose(self) -> ComposeResult:
        with Field("Title"):
            yield Value(id="title")
        with Field("Author"):
            yield List(id="author")
        with Field("Sponsor"):
            yield Value(id="sponsor")
        with Field("Delegate"):
            yield Value(id="delegate")
        with Field("Discussions To"):
            yield List(id="discussions_to")
        with Field("Status"):
            yield List(id="status")
        with Field("Type"):
            yield List(id="type")
        with Field("Topic"):
            yield Value(id="topic")
        with Field("Requires"):
            yield List(id="requires")
        with Field("Replaces"):
            yield List(id="replaces")
        with Field("Superseded By"):
            yield List(id="superseded_by")
        with Field("Created"):
            yield Value(id="created")
        with Field("Python Version"):
            yield List(id="python_versions")
        with Field("Post History"):
            yield List("TODO")
        with Field("Resolution"):
            yield Value("TODO")
        with Field("URL"):
            yield List(id="url")

    @on(DescendantBlur)
    @on(DescendantFocus)
    def _textual_5488_workaround(self) -> None:
        """Workaround for https://github.com/Textualize/textual/issues/5488"""
        for widget in self.query(List):
            widget._refresh_lines()

    def watch_pep(self) -> None:
        """React to the PEP being changed."""
        with self.app.batch_update():
            if self.pep is not None:
                self.query_one("#title", Value).show(self.pep.title)
                self.query_one("#author", List).show(self.pep.authors)
                self.query_one("#sponsor", Value).show(self.pep.sponsor)
                self.query_one("#delegate", Value).show(self.pep.delegate)
                self.query_one("#discussions_to", List).show(self.pep.discussions_to)
                self.query_one("#status", List).show(self.pep.status)
                self.query_one("#type", List).show(self.pep.type)
                self.query_one("#topic", Value).show(self.pep.topic)
                self.query_one("#requires", List).show(self.pep.requires)
                self.query_one("#replaces", List).show(self.pep.replaces)
                self.query_one("#superseded_by", List).show(self.pep.superseded_by)
                self.query_one("#created", Value).show(date_display(self.pep.created))
                self.query_one("#python_versions", List).show(self.pep.python_version)
                self.query_one("#url", List).show(self.pep.url)


### pep_details.py ends here
