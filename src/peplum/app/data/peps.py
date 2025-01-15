"""Provides code for handling a collection of PEPs."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from collections import Counter
from dataclasses import dataclass
from functools import reduce, total_ordering
from operator import concat
from typing import Iterable, Iterator

##############################################################################
# Local imports.
from ...peps import PEP, PEPStatus, PEPType


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
            return self.version > value.version
        raise NotImplementedError

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, PythonVersionCount):
            return self.version == value.version
        raise NotImplementedError


##############################################################################
class PEPs:
    """Class that holds a collection of PEPs."""

    def __init__(self, peps: Iterable[PEP] | None = None) -> None:
        """Initialise the object.

        Args:
            peps: The PEPs to hold.
        """
        self._peps: dict[int, PEP] = (
            {} if peps is None else {pep.number: pep for pep in peps}
        )
        """The PEPs."""

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
                reduce(concat, (pep.python_version or ("",) for pep in self))
            ).items()
        )

    def __contains__(self, pep: PEP | int) -> bool:
        """Is the given PEP in here?"""
        return (pep.number if isinstance(pep, PEP) else pep) in self._peps

    def __iter__(self) -> Iterator[PEP]:
        """The object as an iterator."""
        return iter(self._peps.values())

    def __len__(self) -> int:
        """The count of PEPs in the object."""
        return len(self._peps)


### peps.py ends here
