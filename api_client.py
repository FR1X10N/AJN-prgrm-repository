"""Send a SHA-1 prefix to the HIBP Pwned Passwords range endpoint."""

import http.client
import re
from contextlib import closing


_RANGE_HOST = "api.pwnedpasswords.com"
_TIMEOUT_SECONDS = 5
_MAX_RESPONSE_BYTES = 256 * 1024
_RECORD = re.compile(r"([0-9A-Fa-f]{35}):[0-9]+")


def query_breach_api(prefix: str) -> str | None:
    """Return a valid range response or None when the lookup fails."""
    if not isinstance(prefix, str) or not re.fullmatch(r"[0-9A-Fa-f]{5}", prefix):
        return None

    try:
        # HTTPSConnection verifies certificates by default and follows no redirects.
        with closing(http.client.HTTPSConnection(
            _RANGE_HOST, timeout=_TIMEOUT_SECONDS
        )) as connection:
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
                return None
            body = response.read(_MAX_RESPONSE_BYTES + 1)
            if (
                len(body) > _MAX_RESPONSE_BYTES
                or (response.length is not None and response.length != 0)
            ):
                return None
            text = body.decode("ascii")
    except (OSError, http.client.HTTPException, ValueError):
        return None

    # Reject conflicting or duplicate records before storage builds its mapping.
    seen = set()
    for line in text.splitlines():
        match = _RECORD.fullmatch(line)
        if match is None:
            return None
        suffix = match[1].upper()
        if suffix in seen:
            return None
        seen.add(suffix)

    return text if seen else None
