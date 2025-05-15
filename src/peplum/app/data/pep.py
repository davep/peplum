"""Provides a class for holding data about a PEP."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass, replace
from datetime import date
from re import Pattern, compile
from typing import Any, Final, Literal, cast

##############################################################################
# Local imports.
from .notes import Notes

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
MONTHS: Final[dict[str, int]] = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}
"""Month name to number translation table."""

##############################################################################
PEP_DATE: Final[Pattern[str]] = compile(
    r"^(?P<day>\d{2})-(?P<month>\w{3})-(?P<year>\d{4})$"
)
"""Regular expression for parsing a PEP's date."""


##############################################################################
def parse_date(date_value: str) -> date:
    """Parse the sort of date found in the PEP index.

    Args:
        date_value: The value to parse.

    Returns:
        A `date` object.

    Raises:
        ValueError: If the date string is invalid.

    Notes:
        The dates in the PEP index use a less-than-ideal date format, being
        of the form DD-MMM-YYYY where MMM is a truncated form of the month
        name in English. Because of this this function hand-parses the date
        rather than use strptime, because locales exist and flipping locale
        is problematic for various reasons.
    """
    if parsed_date := PEP_DATE.match(date_value):
        try:
            return date(
                year=int(parsed_date["year"]),
                month=MONTHS[parsed_date["month"].lower()],
                day=int(parsed_date["day"]),
            )
        except KeyError:
            raise ValueError(f"{date_value} is not a recognised date") from None
    else:
        raise ValueError(f"Can't parse {date_value} as a PEP date")


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
    """The number of the PEP."""
    title: str
    """The title of the PEP."""
    authors: str
    """The authors of the PEP."""
    author_names: tuple[str, ...]
    """The names of the authors of the PEP."""
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
    superseded_by: tuple[int, ...]
    """The PEP that supersedes this PEP."""
    url: str
    """The URL for the PEP."""
    notes: str = ""
    """The user's notes associated with this PEP."""

    def annotate(self, *, notes: str | None = None) -> PEP:
        """Annotate the PEP.

        Args:
            notes: The optional notes to annotate the PEP with.
        """
        if notes is not None:
            return replace(self, notes=notes)
        return self

    def __contains__(self, search_text: str) -> bool:
        """Perhaps a case-insensitive search for the text anywhere in the PEP's data.

        Args:
            search_text: The text to search for.

        Returns:
            `True` if the text can be found, `False` if not.
        """
        search_text = search_text.casefold()
        return (
            search_text in str(self.number)
            or search_text in self.title.casefold()
            or search_text in " ".join(self.author_names).casefold()
            or search_text in (self.sponsor or "").casefold()
            or search_text in (self.delegate or "").casefold()
            or search_text in self.status.casefold()
            or search_text in self.type.casefold()
            or search_text in self.topic.casefold()
            or search_text in (str(pep) for pep in self.requires)
            or search_text in str(self.created)
            or search_text in " ".join(str(version) for version in self.python_version)
            or search_text in (str(pep) for pep in self.replaces)
            or search_text in (str(pep) for pep in self.superseded_by)
            or search_text in self.url.casefold()
            or search_text in self.notes.casefold()
        )

    @classmethod
    def _parse(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Parse the content of a PEP from the API data.

        Args:
            data: The data from the PEP API.

        Returns:
            The data turned into locally-useful values.
        """

        def get_ints(field: str) -> tuple[int, ...]:
            if isinstance(values := data[field], str):
                return tuple(int(value) for value in values.split(","))
            return ()

        return dict(
            number=data.get("number", -1),
            title=data.get("title", ""),
            authors=data.get("authors"),
            author_names=tuple(data.get("author_names", [])),
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
            superseded_by=get_ints("superseded_by"),
            url=data.get("url", ""),
        )

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> PEP:
        """Create a PEP from the given API data.

        Args:
            data: The data to create the object from.

        Returns:
            A fresh `PEP` object created from the data.
        """
        return cls(**cls._parse(data))

    @classmethod
    def from_storage(cls, data: dict[str, Any], notes: Notes) -> PEP:
        """Create a PEP from the given data from storage.

        Args:
            data: The data to create the object from.
            notes: The local notes about PEPs.

        Returns:
            A fresh `PEP` object created from the data.
        """
        return cls(**(pep := cls._parse(data)), notes=notes[pep["number"]])


### pep.py ends here
