"""Send a SHA-1 prefix to the HIBP Pwned Passwords range endpoint."""

import http.client
import re
from contextlib import closing


_RANGE_HOST = "api.pwnedpasswords.com"
_TIMEOUT_SECONDS = 5
_MAX_RESPONSE_BYTES = 256 * 1024
_RECORD = re.compile(r"([0-9A-Fa-f]{35}):[0-9]+")


class NetworkError(Exception):
    """The API host could not be reached."""


class APITimeoutError(Exception):
    """The API request timed out."""


class APIResponseError(Exception):
    """The API returned an error or an invalid response."""


def query_breach_api(prefix: str) -> str:
    """Return a valid range response or raise a specific lookup error."""
    if not isinstance(prefix, str) or not re.fullmatch(r"[0-9A-Fa-f]{5}", prefix):
        raise ValueError("Invalid password hash prefix")

    try:
        with closing(
            http.client.HTTPSConnection(
                _RANGE_HOST,
                timeout=_TIMEOUT_SECONDS,
            )
        ) as connection:
            connection.request(
                "GET",
                f"/range/{prefix.upper()}",
                headers={
                    "Add-Padding": "true",
                    "User-Agent": "AJN-pwned.py",
                },
            )
            response = connection.getresponse()

            if response.status != 200:
                raise APIResponseError(
                    f"API returned HTTP {response.status}"
                )

            body = response.read(_MAX_RESPONSE_BYTES + 1)

            if (
                len(body) > _MAX_RESPONSE_BYTES
                or (response.length is not None and response.length != 0)
            ):
                raise APIResponseError("Invalid API response size")

            text = body.decode("ascii")

    except TimeoutError as exc:
        raise APITimeoutError from exc
    except (OSError, http.client.HTTPException) as exc:
        raise NetworkError from exc
    except UnicodeDecodeError as exc:
        raise APIResponseError("API response was not valid ASCII") from exc

    seen = set()
    for line in text.splitlines():
        match = _RECORD.fullmatch(line)
        if match is None:
            raise APIResponseError("API response had an invalid format")

        suffix = match[1].upper()
        if suffix in seen:
            raise APIResponseError("API response contained duplicate records")
        seen.add(suffix)

    if not seen:
        raise APIResponseError("API response contained no records")

    return text

