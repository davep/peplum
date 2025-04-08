"""Provides code for handling a collection of PEPs."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from collections import Counter
from dataclasses import dataclass
from functools import total_ordering
from itertools import chain
from operator import attrgetter
from pathlib import Path
from typing import Iterable, Iterator, Literal, TypeAlias

##############################################################################
# Packaging imports.
from packaging.version import InvalidVersion, Version

##############################################################################
# Typing extensions imports.
from typing_extensions import Self

##############################################################################
# Local imports.
from .locations import data_dir
from .pep import PEP, PEPStatus, PEPType


##############################################################################
def pep_data() -> Path:
    """The path to the local copy of the PEP data."""
    return data_dir() / "peps.json"


##############################################################################
@dataclass(frozen=True)
@total_ordering
class StatusCount:
    """Holds a count of a particular PEP status."""

    status: PEPStatus
    """The PEP status."""
    count: int
    """The count."""

    def __gt__(self, value: object, /) -> bool:
        if isinstance(value, StatusCount):
            return self.status > value.status
        raise NotImplementedError

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, StatusCount):
            return self.status == value.status
        raise NotImplementedError


##############################################################################
@dataclass(frozen=True)
@total_ordering
class TypeCount:
    """Holds a count of a particular PEP type."""

    type: PEPType
    """The PEP type."""
    count: int
    """The count."""

    def __gt__(self, value: object, /) -> bool:
        if isinstance(value, TypeCount):
            return self.type > value.type
        raise NotImplementedError

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, TypeCount):
            return self.type == value.type
        raise NotImplementedError


##############################################################################
@dataclass(frozen=True)
@total_ordering
class PythonVersionCount:
    """Holds a count of a particular PEP python version."""

    version: str
    """The Python version."""
    count: int
    """The count."""

    def __gt__(self, value: object, /) -> bool:
        if isinstance(value, PythonVersionCount):
            try:
                return Version(self.version) > Version(value.version)
            except InvalidVersion:
                return self.version > value.version
        raise NotImplementedError

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, PythonVersionCount):
            try:
                return Version(self.version) == Version(value.version)
            except InvalidVersion:
                return self.version == value.version
        raise NotImplementedError


##############################################################################
@dataclass(frozen=True)
@total_ordering
class AuthorCount:
    """Holds a count of a particular PEP author."""

    author: str
    """The PEP author."""
    count: int
    """The count."""

    def __gt__(self, value: object, /) -> bool:
        if isinstance(value, AuthorCount):
            return self.author.casefold() > value.author.casefold()
        raise NotImplementedError

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, AuthorCount):
            return self.author.casefold() == value.author.casefold()
        raise NotImplementedError


##############################################################################
PEPCount: TypeAlias = StatusCount | TypeCount | PythonVersionCount | AuthorCount
"""The type of the various counts."""

##############################################################################
Filters: TypeAlias = tuple["Filter", ...]
"""The type of a collection of filters."""


##############################################################################
class Filter:
    """Base class for the raindrop filters."""

    def __rand__(self, _: PEP) -> bool:
        return False

    def __radd__(self, filters: Filters) -> Filters:
        return (*filters, self)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, self.__class__):
            return str(value) == str(self)
        return False


##############################################################################
class WithStatus(Filter):
    """Filter on a PEP's status."""

    def __init__(self, status: PEPStatus) -> None:
        """Initialise the object.

        Args:
            status: The status to filter on.
        """
        self._status = status
        """The status to filter on."""

    def __rand__(self, pep: PEP) -> bool:
        return pep.status == self._status

    def __str__(self) -> str:
        return str(self._status)


##############################################################################
class WithType(Filter):
    """Filter on a PEP's status."""

    def __init__(self, pep_type: PEPType) -> None:
        """Initialise the object.

        Args:
            pep_type: The type to filter on.
        """
        self._type = pep_type
        """The type to filter on."""

    def __rand__(self, pep: PEP) -> bool:
        return pep.type == self._type

    def __str__(self) -> str:
        return str(self._type)


##############################################################################
class WithPythonVersion(Filter):
    """Filter on a PEP's Python version."""

    def __init__(self, version: str) -> None:
        """Initialise the object.

        Args:
            version: The version to filter on.
        """
        self._version = version
        """The type to filter on."""

    def __rand__(self, pep: PEP) -> bool:
        return (
            self._version in pep.python_version
            if self._version
            else not pep.python_version
        )

    def __str__(self) -> str:
        return self._version or "None"


##############################################################################
class WithAuthor(Filter):
    """Filter on a PEP's author."""

    def __init__(self, author: str) -> None:
        """Initialise the object.

        Args:
            author: The author to filter on.
        """
        self._author = author
        """The author to filter on."""
        self._folded_author = author.casefold()
        """The folded version of the author for case-insensitive lookup."""

    def __rand__(self, pep: PEP) -> bool:
        return self._folded_author in (author.casefold() for author in pep.author_names)

    def __str__(self) -> str:
        return str(self._author)


##############################################################################
class Containing(Filter):
    """Filter on text found within a PEP's data."""

    def __init__(self, text: str) -> None:
        """Initialise the object.

        Args:
            text: The text to filter on.
        """
        self._text = text
        """The text to look for."""

    def __rand__(self, pep: PEP) -> bool:
        return self._text in pep

    def __str__(self) -> str:
        return self._text

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Containing):
            return str(value).casefold() == self._text.casefold()
        return super().__eq__(value)


##############################################################################
SortOrder: TypeAlias = Literal["number", "created", "title"]
"""Sort orders for PEPs."""


##############################################################################
class PEPs:
    """Class that holds a collection of PEPs."""

    def __init__(
        self,
        peps: Iterable[PEP] | None = None,
        filters: Filters | None = None,
        sort_order: SortOrder = "number",
        sort_reversed: bool = False,
    ) -> None:
        """Initialise the object.

        Args:
            peps: The PEPs to hold.
            filters: The filters that got to this set of PEPs.
            sort_order: The sort order for the PEPs.
            sort_reversed: Should the sort order be reversed?
        """
        self._peps: dict[int, PEP] = (
            {} if peps is None else {pep.number: pep for pep in peps}
        )
        """The PEPs."""
        self._filters = () if filters is None else filters
        """The filters that got to this set of PEPs."""
        self._sort_order: SortOrder = sort_order
        """The sort order for the PEPs."""
        self._sort_reversed = sort_reversed
        """Should we reverse the sort order?"""

    def patch_pep(self, pep: PEP) -> Self:
        """Patch a PEP with a new instance.

        Args:
            pep: The new PEP.

        Returns:
            Self.
        """
        self._peps[pep.number] = pep
        return self

    @property
    def is_filtered(self) -> bool:
        """Does this collection of PEPs have a filter?"""
        return bool(self._filters)

    @property
    def statuses(self) -> tuple[StatusCount, ...]:
        """The status and their counts as found in the PEPs."""
        return tuple(
            StatusCount(status, count)
            for status, count in Counter[PEPStatus](pep.status for pep in self).items()
        )

    @property
    def types(self) -> tuple[TypeCount, ...]:
        """The types and their counts as found in the PEPs."""
        return tuple(
            TypeCount(pep_type, count)
            for pep_type, count in Counter[PEPType](pep.type for pep in self).items()
        )

    @property
    def python_versions(self) -> tuple[PythonVersionCount, ...]:
        """The Python versions and their counts as found in the PEPs.

        Notes:
            A count for an empty string is included, this is the count of
            PEPs that have no Python version associated with them.
        """
        return tuple(
            PythonVersionCount(version, count)
            for version, count in Counter(
                chain(*(pep.python_version or ("",) for pep in self))
            ).items()
        )

    @property
    def authors(self) -> tuple[AuthorCount, ...]:
        """The authors and their counts as found in the PEPs."""
        return tuple(
            AuthorCount(author, count)
            for author, count in Counter(
                chain(*(pep.author_names for pep in self))
            ).items()
        )

    def _describe(self, name: str, filter_type: type[Filter]) -> str | None:
        """Describe the user's use of a particular filter.

        Args:
            name: The name to give the filter.
            filter_type: The type of filter to look for.

        Returns:
            A description if the filter is used, or `None`.
        """
        return (
            f"{name} {' and '.join(filters)}"
            if (
                filters := [
                    f"{candidate}"
                    for candidate in self._filters
                    if isinstance(candidate, filter_type)
                ]
            )
            else None
        )

    @property
    def description(self) -> str:
        """The description of the content of the PEPs collection."""
        filters = [
            candidate
            for candidate in [
                self._describe(name, filter_type)
                for name, filter_type in (
                    ("Containing", Containing),
                    ("Type", WithType),
                    ("Status", WithStatus),
                    ("Version", WithPythonVersion),
                    ("Author", WithAuthor),
                )
            ]
            if candidate
        ] or ["All"]

        match self._sort_order:
            case "number":
                sort_order = "PEP Number"
            case "created":
                sort_order = "Date Created"
            case "title":
                sort_order = "PEP Title"

        if self._sort_reversed:
            sort_order += " (reversed)"

        return "; ".join(filters + ([f"Sorted by {sort_order}"] if sort_order else []))

    def __and__(self, new_filter: Filter) -> PEPs:
        """Get the PEPs match a given filter.

        Args:
            new_filter: The new filter to apply.

        Returns:
            The subset of PEPs that match the given filter.
        """
        # Only return a new PEPs object if the filter we've been given isn't
        # already active.
        return (
            self
            if new_filter in self._filters
            else PEPs(
                (pep for pep in self if pep & new_filter),
                self._filters + new_filter,
                self._sort_order,
                self._sort_reversed,
            )
        )

    def sorted_by(self, sort_order: SortOrder) -> PEPs:
        """Get the PEPs sorted in a particular way.

        Args:
            The sort order.

        Returns:
            The PEPs sorted in the required way.
        """
        return PEPs(self, self._filters, sort_order, self._sort_reversed)

    def reversed(self, setting: bool | None = None) -> PEPs:
        """Get the PEPs with the current sort order reversed.

        Args:
            setting: Optional specific setting.

        Returns:
            The PEPs sorted in the required order.

        Notes:
            If no value is given, the direction will be reversed from what
            it is now, otherwise `True` will be forward sort order, `False`
            will be reversed.
        """
        return PEPs(
            self,
            self._filters,
            self._sort_order,
            not self._sort_reversed if setting is None else setting,
        )

    def rebuild_from(self, peps: PEPs) -> PEPs:
        """Rebuild a collection of PEPs from a given collection.

        Given a collection of PEPs, filter it by this PEPs' filters, sort by
        this PEPs' sort order, then return the fresh collection.

        Args:
            peps: The PEPs to seed the rebuild.

        Returns:
            The new collection of PEPs.
        """
        return PEPs(
            (pep for pep in peps if all(pep & check for check in self._filters)),
            self._filters,
            self._sort_order,
            self._sort_reversed,
        )

    def __contains__(self, pep: PEP | int) -> bool:
        """Is the given PEP in here?"""
        return (pep.number if isinstance(pep, PEP) else pep) in self._peps

    def __iter__(self) -> Iterator[PEP]:
        """The object as an iterator."""
        return iter(
            sorted(
                self._peps.values(),
                key=attrgetter(self._sort_order),
                reverse=self._sort_reversed,
            )
        )

    def __len__(self) -> int:
        """The count of PEPs in the object."""
        return len(self._peps)


### peps.py ends here
