"""Provides a PEP API client class."""

##############################################################################
# Python imports.
from pathlib import Path
from ssl import SSLCertVerificationError
from typing import Any, Final

##############################################################################
# HTTPX imports.
from httpx import AsyncClient, HTTPStatusError, RequestError, Response


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

    async def _get(self, url: str) -> Response:
        """Make a GET request.

        Args:
            url: The URL to make the request of.

        Returns:
            The response.

        Raises:
            RequestError: If there was some sort of error.
        """
        try:
            response = await self._client.get(url, headers={"user-agent": self.AGENT})
        except (RequestError, SSLCertVerificationError) as error:
            raise self.RequestError(str(error)) from None

        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            raise self.RequestError(str(error)) from None

        return response

    async def get_peps(self) -> dict[int, dict[str, Any]]:
        """Download a fresh list of all known PEPs.

        Returns:
            The PEP JSON data.

        Raises:
            RequestError: If there was a problem getting the PEPS.
        """
        if isinstance(
            raw_data := (
                await self._get("https://peps.python.org/api/peps.json")
            ).json(),
            dict,
        ):
            return raw_data
        raise RequestError("Unexpected data received from the PEP API")

    @staticmethod
    def pep_file(pep: int) -> Path:
        """Generate the name of the source file of a PEP.

        Args:
            pep: The number of the PEP.

        Returns:
            The name of the source file for that PEP.
        """
        return Path(f"pep-{pep:04}.rst")

    @classmethod
    def pep_url(cls, pep: int) -> str:
        """Generate the URL for the source of a PEP.

        Args:
            pep: The number of the PEP.

        Returns:
            The URL for the source of the PEP.
        """
        return f"https://raw.githubusercontent.com/python/peps/refs/heads/main/peps/{cls.pep_file(pep)}"

    async def get_pep(self, pep: int) -> str:
        """Download the text of a given PEP.

        Args:
            pep: The number of the PEP to download.

        Returns:
            The text for the PEP.
        """
        return (await self._get(self.pep_url(pep))).text


### api.py ends here
