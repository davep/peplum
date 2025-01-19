"""Provides a widget for showing a PEP's details."""

##############################################################################
# Python imports.
from datetime import date, datetime

##############################################################################
# Humanize imports
from humanize import naturaltime

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.reactive import var
from textual.widgets import Label, OptionList

##############################################################################
# Local imports.
from ...peps import PEP


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
        &.hidden {
            display: none;
        }
    }
    """

    def __init__(self, title: str) -> None:
        """Initialise the widget.

        Args:
            title: The title to give the widget.
        """
        super().__init__()
        self.compose_add_child(Label(f"{title}:"))


##############################################################################
class HidableValue(Label):
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
class URL(HidableValue, can_focus=True):
    """A widget that is a clickable URL that can also be focused."""

    DEFAULT_CSS = """
    URL {
        &:focus {
            color: $block-cursor-foreground;
            background: $block-cursor-background;
        }
    }
    """


##############################################################################
class List(OptionList):
    """Show a list of values that the user can pick from."""

    def show(self, options: tuple[str | int, ...]) -> None:
        """Show the list.

        Args:
            options: The options to show.
        """
        if self.parent is None:
            return
        self.parent.set_class(not bool(options), "hidden")
        self.clear_options().add_options([str(option) for option in options])


##############################################################################
class PEPDetails(VerticalScroll):
    """A widget for showing details of a PEP."""

    DEFAULT_CSS = """
    PEPDetails {
        Markdown {
            padding: 0 1 0 1;
            background: transparent;
            MarkdownH2 {
                margin: 0;
            }
        }
    }
    """

    pep: var[PEP | None] = var(None)
    """The PEP to show the details of."""

    def compose(self) -> ComposeResult:
        with Field("Title"):
            yield Label(id="title")
        with Field("Author"):
            yield List(id="author")
        with Field("Sponsor"):
            yield HidableValue(id="sponsor")
        with Field("Delegate"):
            yield HidableValue(id="delegate")
        with Field("Discussions To"):
            yield URL(id="discussions_to")
        with Field("Status"):
            yield Label(id="status")
        with Field("Type"):
            yield Label(id="type")
        with Field("Topic"):
            yield HidableValue(id="topic")
        with Field("Requires"):
            yield List(id="requires")
        with Field("Replaces"):
            yield List(id="replaces")
        with Field("Superseded By"):
            yield HidableValue(id="superseded_by")
        with Field("Created"):
            yield Label(id="created")
        with Field("Python Version"):
            yield List(id="python_versions")
        with Field("Post History"):
            yield Label("TODO")
        with Field("Resolution"):
            yield Label("TODO")
        with Field("URL"):
            yield URL(id="url")

    def watch_pep(self) -> None:
        """React to the PEP being changed."""
        with self.app.batch_update():
            self.border_title = (
                f"PEP {self.pep.number}" if self.pep is not None else "No PEP selected"
            )
            self.query_one(Field).set_class(self.pep is None, "hidden")
            if self.pep is not None:
                self.query_one("#title", Label).update(self.pep.title)
                self.query_one("#author", List).show(self.pep.authors)
                self.query_one("#sponsor", HidableValue).show(self.pep.sponsor)
                self.query_one("#delegate", HidableValue).show(self.pep.delegate)
                self.query_one("#discussions_to", URL).show(self.pep.discussions_to)
                self.query_one("#status", Label).update(self.pep.status)
                self.query_one("#type", Label).update(self.pep.type)
                self.query_one("#topic", HidableValue).show(self.pep.topic)
                self.query_one("#requires", List).show(self.pep.requires)
                self.query_one("#replaces", List).show(self.pep.replaces)
                self.query_one("#superseded_by", HidableValue).show(
                    self.pep.superseded_by
                )
                self.query_one("#created", Label).update(date_display(self.pep.created))
                self.query_one("#python_versions", List).show(self.pep.python_version)
                self.query_one("#url", URL).show(self.pep.url)


### pep_details.py ends here
