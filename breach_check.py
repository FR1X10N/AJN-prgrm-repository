"""Orchestrate one HIBP check using local hashing and temporary storage."""

from pathlib import Path
from tempfile import TemporaryDirectory

from password import hash_and_split_password
from api_client import (
    APIResponseError,
    APITimeoutError,
    NetworkError,
    query_breach_api,
)


def check_password_once(password: bytearray) -> str:
    try:
        from storage import (
            check_suffix_in_response,
            delete_api_response,
            save_api_response,
        )

        prefix, suffix = hash_and_split_password(password)

        try:
            response = query_breach_api(prefix)
        except NetworkError:
            return "NETWORK_ERROR"
        except APITimeoutError:
            return "API_TIMEOUT"
        except APIResponseError:
            return "API_ERROR"

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
        return "CHECK_ERROR"

    return "CHECK_ERROR"
