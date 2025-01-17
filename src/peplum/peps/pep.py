"""Provides a class for holding data about a PEP."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from datetime import date, datetime
from locale import LC_TIME, getlocale, setlocale
from re import Pattern, compile
from typing import Any, Final, Literal, cast

##############################################################################
PEPStatus = Literal[
    "Draft",
    "Active",
    "Accepted",
    "Provisional",
    "Deferred",
    "Rejected",
    "Withdrawn",
    "Final",
    "Superseded",
]
"""The possible status values for a PEP."""

##############################################################################
PEPType = Literal[
    "Standards Track",
    "Informational",
    "Process",
]
"""The possible types of PEP."""


##############################################################################
def parse_date(date_value: str) -> date:
    """Parse the sort of date found in the PEP index.

    Args:
        date_value: The value to parse.

    Returns:
        A `date` object.

    Notes:
        The dates in the PEP index use a less-than-ideal date format, being
        of the form DD-MMM-YYYY where MMM is a truncated form of the month
        name in English. With this in mind the locale is set in the hope
        that it'll help with the parsing with strptime.
    """
    save_locale = getlocale(LC_TIME)
    try:
        setlocale(LC_TIME, "en_US")
        return datetime.strptime(date_value, "%d-%b-%Y").date()
    finally:
        setlocale(LC_TIME, save_locale)


##############################################################################
DATE_ONLY: Final[Pattern[str]] = compile(r"^\d{2}-\w{3}-\d{4}$")
"""Regular expression for detecting just a date in the input."""
URL_ONLY: Final[Pattern[str]] = compile("^http")
"""Regular expression for detecting just an URL in the input."""
DATE_AND_URL: Final[Pattern[str]] = compile(
    r"^`(?P<date>\d{2}-\w{3}-\d{4}).+<(?P<url>https:.*)>`__$"
)
"""Regular expression for detecting a date and URL in the input."""


##############################################################################
@dataclass(frozen=True)
class PostHistory:
    """Details of an item in a PEP's post history."""

    date: date | None = None
    """The date of the post history."""
    url: str | None = None
    """The URL of a link to the post, if there is one."""

    @classmethod
    def from_value(cls, value: str | None) -> PostHistory | None:
        """Create a post history object from the given value.

        Args:
            value: The value to create the history from.

        Returns:
            A `PostHistory` instance, or `None` if `None` was the input.
        """
        if value is None:
            return value
        if match := DATE_ONLY.match(value):
            return PostHistory(date=parse_date(value))
        if match := URL_ONLY.match(value):
            return PostHistory(url=value)
        if match := DATE_AND_URL.match(value):
            return PostHistory(date=parse_date(match["date"]), url=match["url"])
        raise ValueError(f"Can't parse `{value}` as PostHistory")


##############################################################################
@dataclass(frozen=True)
class PEP:
    """A class that holds data about a PEP."""

    number: int
    """The numbe of the PEP."""
    title: str
    """The title of the PEP."""
    authors: tuple[str, ...]
    """The authors of the PEP."""
    sponsor: str | None
    """The sponsor of the PEP."""
    delegate: str | None
    """The name of the PEP's delegate."""
    discussions_to: str | None
    """The location where discussions about this PEP should take place."""
    status: PEPStatus
    """The status of the PEP."""
    type: PEPType
    """The type of the PEP."""
    topic: str
    """The topic of the PEP."""
    requires: tuple[int, ...]
    """The PEPS that this PEP requires."""
    created: date
    """The date the PEP was created."""
    python_version: tuple[str, ...]
    """The Python versions this PEP relates to."""
    post_history: tuple[PostHistory, ...]
    """The dates of the posting history for the PEP."""
    resolution: PostHistory | None
    """The resolution of the PEP, if it has one."""
    replaces: tuple[int, ...]
    """The PEPs this PEP replaces."""
    superseded_by: int | None
    """The PEP that supersedes this PEP."""
    url: str
    """The URL for the PEP."""

    _AUTHOR_SPLIT = compile(r",(?! +Jr)")
    """The regular expression for splitting up authors.

    Notes:
        This is 'good enough' but not ideal. It might need updating and
        improvement later on.
    """

    @classmethod
    def _authors(cls, authors: str) -> tuple[str, ...]:
        """Get the authors from a string.

        Args:
            authors: The authors to parse.

        Returns:
            A tuple of the authors found.

        Notes:
            The authors in the PEPs are a comma-separated string of author
            names. The problem is, as of the time of writing, there's at
            least one author who has a comma in their name. So this method
            makes an effort to split up the authors while also keeping such
            a name intact.

            Yes, this is going to be brittle.

            Yes, the code here is a bit of a hack.

            https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
        """
        return tuple(author.strip() for author in cls._AUTHOR_SPLIT.split(authors))

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> PEP:
        """Create a PEP from the given JSON data.

        Args:
            data: The data to create the object from.

        Returns:
            A fresh `PEP` object created from the data.
        """

        def get_ints(field: str) -> tuple[int, ...]:
            if isinstance(values := data[field], str):
                return tuple(int(value) for value in values.split(","))
            return ()

        return cls(
            number=data.get("number", -1),
            title=data.get("title", ""),
            authors=cls._authors(data.get("authors", "")),
            sponsor=data.get("sponsor"),
            delegate=data.get("delegate"),
            discussions_to=data.get("discussions_to"),
            status=cast(PEPStatus, data.get("status")),
            type=cast(PEPType, data.get("type")),
            topic=data.get("topic", ""),
            requires=get_ints("requires"),
            created=parse_date(data.get("created", "")),
            python_version=tuple(
                version.strip()
                for version in (data.get("python_version") or "").split(",")
                if version
            ),
            post_history=tuple(
                PostHistory.from_value(post.strip()) or PostHistory()
                for post in (data.get("post_history", "") or "").split(",")
                if post
            ),
            resolution=PostHistory.from_value(data.get("resolution")),
            replaces=get_ints("replaces"),
            superseded_by=None
            if data.get("superseded_by") is None
            else int(data["superseded_by"]),
            url=data.get("url", ""),
        )


### pep.py ends here
