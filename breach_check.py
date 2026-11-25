"""Orchestrate one HIBP check using local hashing and temporary storage."""

from pathlib import Path
from tempfile import TemporaryDirectory

from api_client import query_breach_api
from password import hash_and_split_password


def check_password_once(password: bytearray) -> str:
    """Return BREACHED, NOT_FOUND, or UNKNOWN without altering the input buffer.""" # We should also agree on whether the check should return the breach count, in addition to the status (`BREACHED`, `NOT_FOUND`, or `UNKNOWN`).
    try:
        # Storage is delivered on the team's separate Ali modules branch.
        from storage import (
            check_suffix_in_response,
            delete_api_response,
            save_api_response,
        )

        prefix, suffix = hash_and_split_password(password)
        response = query_breach_api(prefix)
        if response is None:
            return "UNKNOWN"

        with TemporaryDirectory(prefix="pwned-") as directory:
            path = Path(directory) / "range.json"
            try:
                save_api_response(response, path)
                result = check_suffix_in_response(suffix, path)
                if result in ("BREACHED", "NOT_FOUND"):
                    return result
            finally:
                delete_api_response(path)
    except (ImportError, OSError, TypeError, ValueError):
        return "UNKNOWN"

    return "UNKNOWN"
