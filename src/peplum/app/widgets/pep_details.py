"""Provides a widget for showing a PEP's details."""

##############################################################################
# Python imports.
from datetime import date, datetime
from functools import singledispatchmethod
from typing import Sequence
from webbrowser import open as visit_url

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
from textual.widgets.option_list import Option

##############################################################################
# Local imports.
from ...peps import PEP, PEPStatus, PEPType, PostHistory
from ..messages import GotoPEP, ShowAuthor, ShowStatus, ShowType, VisitPEP
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
class Item(Option):
    """Type of an item that goes in a list."""

    def select(self, parent: OptionListEx) -> None:
        """Perform the selection action for the item.

        Args:
            parent: The parent list for the item.
        """


##############################################################################
class StatusItem(Item):
    """Type of an item that is a PEP status."""

    def __init__(self, status: PEPStatus) -> None:
        """Initialise the object.

        Args:
            status: The status.
        """
        self._status: PEPStatus = status
        super().__init__(status)

    def select(self, parent: OptionListEx) -> None:
        """Perform the selection action for the item.

        Args:
            parent: The parent list for the item.
        """
        parent.post_message(ShowStatus(self._status))


##############################################################################
class TypeItem(Item):
    """Type of an item that is a PEP type."""

    def __init__(self, pep_type: PEPType) -> None:
        """Initialise the object.

        Args:
            pep_type: The PEP type.
        """
        self._type: PEPType = pep_type
        super().__init__(pep_type)

    def select(self, parent: OptionListEx) -> None:
        """Perform the selection action for the item.

        Args:
            parent: The parent list for the item.
        """
        parent.post_message(ShowType(self._type))


##############################################################################
class PEPItem(Item):
    """Type of an item that is a PEP number."""

    def __init__(self, pep: int) -> None:
        """Initialise the object.

        Args:
            pep: The number of the pep.
        """
        self._pep = pep
        super().__init__(f"PEP{pep}")

    def select(self, parent: OptionListEx) -> None:
        """Perform the selection action for the item.

        Args:
            parent: The parent list for the item.
        """
        parent.post_message(GotoPEP(self._pep))


##############################################################################
class AuthorItem(Item):
    """Type of an item that shows an author."""

    def __init__(self, author: str) -> None:
        """Initialise the object.

        Args:
            author: The author.
        """
        self._author = author
        super().__init__(author)

    def select(self, parent: OptionListEx) -> None:
        """Perform the selection action for the item.

        Args:
            parent: The parent list for the item.
        """
        parent.post_message(ShowAuthor(self._author))


##############################################################################
class URLItem(Item):
    """Type of an item that shows a URL."""

    def __init__(self, url: str, title: str | None = None) -> None:
        """Initialise the object.

        Args:
            url: The URL.
            title: An optional title for the URL.
        """
        self._url = url
        super().__init__(title or url)

    def select(self, parent: OptionListEx) -> None:
        """Perform the selection action for the item.

        Args:
            parent: The parent list for the item.
        """
        visit_url(self._url)


##############################################################################
class PostItem(Item):
    """Type of an item that is a post."""

    def __init__(self, post: PostHistory) -> None:
        """Initialise the object.

        Args:
            post: The post.
        """
        self._post = post
        super().__init__(post.title)

    def select(self, parent: OptionListEx) -> None:
        """Perform the selection action for the item.

        Args:
            parent: The parent list for the item.
        """
        if self._post.url:
            visit_url(self._post.url)
        else:
            parent.notify("There is no URL associated with this.", title="No URL")


##############################################################################
class ClickableValue(OptionListEx):
    """Show a value that the user can interact with."""

    DEFAULT_CSS = """
    ClickableValue, ClickableValue:focus {
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
    def show(self, values: Sequence[Item | None]) -> None:
        """Show a list of values.

        Args:
            values: The values to show.

        Notes:
            Any values that are empty will be removed. If the list is empty
            after this filter the field will be hidden.
        """
        if self.parent is None:
            return
        self.clear_options().add_options([value for value in values if value])
        self.parent.set_class(not bool(self.option_count), "hidden")

    @show.register
    def _(self, values: Item | None) -> None:
        """Show a single value."""
        self.show([values])

    def on_focus(self) -> None:
        """Ensure the highlight appears when we get focus."""
        if self.highlighted is None and self.option_count:
            self.highlighted = 0

    def on_blur(self) -> None:
        """Remove the highlight when we no longer have focus."""
        self.highlighted = None

    @on(OptionListEx.OptionSelected)
    def select(self, message: OptionListEx.OptionSelected) -> None:
        assert isinstance(message.option, Item)
        message.option.select(self)


##############################################################################
class PEPDetails(VerticalScroll):
    """A widget for showing details of a PEP."""

    pep: var[PEP | None] = var(None)
    """The PEP to show the details of."""

    BINDINGS = [("enter", "visit_pep")]

    def compose(self) -> ComposeResult:
        with Field("Title"):
            yield Value(id="title")
        with Field("Author"):
            yield ClickableValue(id="author")
        with Field("Sponsor"):
            yield Value(id="sponsor")
        with Field("Delegate"):
            yield Value(id="delegate")
        with Field("Discussions To"):
            yield Value(id="discussions_to")
        with Field("Status"):
            yield ClickableValue(id="status")
        with Field("Type"):
            yield ClickableValue(id="type")
        with Field("Topic"):
            yield Value(id="topic")
        with Field("Requires"):
            yield ClickableValue(id="requires")
        with Field("Replaces"):
            yield ClickableValue(id="replaces")
        with Field("Superseded By"):
            yield ClickableValue(id="superseded_by")
        with Field("Created"):
            yield Value(id="created")
        with Field("Python Version"):
            yield ClickableValue(id="python_versions")
        with Field("Post History"):
            yield ClickableValue(id="post_history")
        with Field("Resolution"):
            yield ClickableValue(id="resolution")
        with Field("URL"):
            yield ClickableValue(id="url")

    @on(DescendantBlur)
    @on(DescendantFocus)
    def _textual_5488_workaround(self) -> None:
        """Workaround for https://github.com/Textualize/textual/issues/5488"""
        for widget in self.query(ClickableValue):
            widget._refresh_lines()

    def watch_pep(self) -> None:
        """React to the PEP being changed."""
        with self.app.batch_update():
            if self.pep is not None:
                self.query_one("#title", Value).show(self.pep.title)
                self.query_one("#author", ClickableValue).show(
                    [AuthorItem(author) for author in self.pep.authors]
                )
                self.query_one("#sponsor", Value).show(self.pep.sponsor)
                self.query_one("#delegate", Value).show(self.pep.delegate)
                self.query_one("#discussions_to", Value).show(self.pep.discussions_to)
                self.query_one("#status", ClickableValue).show(
                    StatusItem(self.pep.status)
                )
                self.query_one("#type", ClickableValue).show(TypeItem(self.pep.type))
                self.query_one("#topic", Value).show(self.pep.topic)
                self.query_one("#requires", ClickableValue).show(
                    [PEPItem(pep) for pep in self.pep.requires]
                )
                self.query_one("#replaces", ClickableValue).show(
                    [PEPItem(pep) for pep in self.pep.replaces]
                )
                self.query_one("#superseded_by", ClickableValue).show(
                    None
                    if self.pep.superseded_by is None
                    else PEPItem(self.pep.superseded_by)
                )
                self.query_one("#created", Value).show(date_display(self.pep.created))
                self.query_one("#python_versions", ClickableValue).show(
                    self.pep.python_version
                )
                self.query_one("#post_history", ClickableValue).show(
                    [PostItem(post) for post in self.pep.post_history]
                )
                self.query_one("#resolution", ClickableValue).show(
                    None
                    if self.pep.resolution is None
                    else PostItem(self.pep.resolution)
                )
                self.query_one("#url", ClickableValue).show(URLItem(self.pep.url))

    def action_visit_pep(self) -> None:
        """Action that visits the current PEP."""
        if self.pep is not None:
            self.post_message(VisitPEP(self.pep))


### pep_details.py ends here
