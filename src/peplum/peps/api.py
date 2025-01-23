"""Provides a PEP API client class."""

##############################################################################
# Python imports.
from ssl import SSLCertVerificationError
from typing import Any, Final

##############################################################################
# HTTPX imports.
from httpx import AsyncClient, HTTPStatusError, RequestError

##############################################################################
# Local imports.
from .pep import PEP


##############################################################################
class API:
    """API client for peps.python.org."""

    AGENT: Final[str] = "Peplum (https://github.com/davep/peplum)"
    """The agent string to use when talking to the API."""

    _URL: Final[str] = "https://peps.python.org/api/peps.json"
    """The URL of the PEP download API."""

    class Error(Exception):
        """Base class for Raindrop errors."""

    class RequestError(Error):
        """Exception raised if there was a problem making an API request."""

    def __init__(self) -> None:
        """Initialise the client object."""
        self._client_: AsyncClient | None = None
        """The internal reference to the HTTPX client."""

    @property
    def _client(self) -> AsyncClient:
        """The HTTPX client."""
        if self._client_ is None:
            self._client_ = AsyncClient()
        return self._client_

    async def get_peps(self) -> tuple[list[PEP], dict[int, dict[str, Any]]]:
        """Download a fresh list of all known PEPs.

        Returns:
            A tuple of a list of all known PEPs and the raw JSON they were
            created from.
        """
        try:
            response = await self._client.get(
                self._URL, headers={"user-agent": self.AGENT}
            )
        except (RequestError, SSLCertVerificationError) as error:
            raise self.RequestError(str(error)) from None

        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            raise self.RequestError(str(error)) from None

        return [PEP.from_json(pep) for pep in response.json().values()], response.json()


### api.py ends here
