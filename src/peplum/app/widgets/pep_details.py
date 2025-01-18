"""Provides a widget for showing a PEP's details."""

##############################################################################
# Python imports.
from datetime import datetime
from inspect import cleandoc

##############################################################################
# Humanize imports
from humanize import naturaltime

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import var
from textual.widgets import Markdown

##############################################################################
# Local imports.
from ...peps import PEP, PostHistory


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
        yield Markdown()

    @staticmethod
    def post_as_markdown(post: PostHistory) -> str:
        """Format a post for Markdown.

        Args:
            post: The post to format.

        Returns:
            The formatted post.
        """
        if post.date and not post.url:
            return f"{post.date} ({naturaltime(datetime.combine(post.date, datetime.min.time()))})"
        if not post.date and post.url:
            return post.url
        assert post.date is not None  # It really is not None here.
        return f"[{post.date} ({naturaltime(datetime.combine(post.date, datetime.min.time()))})]({post.url})"

    @property
    def pep_post_history_as_markdown(self) -> str:
        """The PEP's post history as Markdown."""
        if not self.pep or not self.pep.post_history:
            return ""
        return ", ".join(self.post_as_markdown(post) for post in self.pep.post_history)

    @property
    def pep_as_markdown(self) -> str:
        """The PEP as Markdown."""

        if self.pep is None:
            return "No PEP selected"

        return cleandoc(f"""
        # {self.pep.title}

        ## Author{"" if len(self.pep.authors) == 1 else "s"}
        {", ".join(self.pep.authors)}

        {"## Sponsor" if self.pep.sponsor else ""}
        {self.pep.sponsor or ""}

        {"## Delegate" if self.pep.delegate else ""}
        {self.pep.delegate or ""}

        {"## Discussions to" if self.pep.discussions_to else ""}
        {self.pep.discussions_to or ""}

        ## Status
        {self.pep.status}

        ## Type
        {self.pep.type}

        {"## Topic" if self.pep.topic else ""}
        {(self.pep.topic or "").capitalize()}

        {"## Requires" if self.pep.requires else ""}
        {", ".join(str(pep) for pep in self.pep.requires) or ""}

        {"## Replaces" if self.pep.replaces else ""}
        {", ".join(str(pep) for pep in self.pep.replaces) or ""}

        {"## Superseded By" if self.pep.superseded_by is not None else ""}
        {"" if self.pep.superseded_by is None else self.pep.superseded_by}

        ## Created
        {self.pep.created} - {naturaltime(datetime.combine(self.pep.created, datetime.min.time()))}

        {"## Python Version" if self.pep.python_version else ""}
        {", ".join(self.pep.python_version) or ""}

        {"## Post History" if self.pep.post_history else ""}
        {self.pep_post_history_as_markdown.strip()}

        {"## Resolution" if self.pep.resolution else ""}
        {"" if self.pep.resolution is None else self.post_as_markdown(self.pep.resolution)}

        ## URL
        {self.pep.url}
        """)

    def watch_pep(self) -> None:
        """React to the PEP being changed."""
        self.border_title = (
            f"PEP {self.pep.number}" if self.pep is not None else "No PEP selected"
        )
        self.query_one(Markdown).update(self.pep_as_markdown)


### pep_details.py ends here
