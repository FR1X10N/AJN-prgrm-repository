"""Read, hash, and generate passwords using the standard library."""

import getpass
import hashlib
import secrets
import string
import warnings
from collections.abc import Callable


def read_password(prompt: str = "Password: ") -> bytearray:
    """Read hidden input as a mutable UTF-8 buffer or stop safely."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            return bytearray(getpass.getpass(prompt), "utf-8")
    except (getpass.GetPassWarning, EOFError, OSError, UnicodeError):
        raise SystemExit("Could not read a password securely.") from None


def wipe_password(buffer: bytearray) -> None:
    """Zero the buffer in place. Python's internal copies may remain."""
    for index in range(len(buffer)):
        buffer[index] = 0


def hash_and_split_password(password: bytearray) -> tuple[str, str]:
    """Return the uppercase SHA-1 prefix and suffix required by HIBP."""
    digest = hashlib.sha1(password, usedforsecurity=False).hexdigest().upper()
    return digest[:5], digest[5:]


def generate_password(policy: dict | None) -> bytearray:
    """Generate a mutable candidate using the policy's length and exclusions."""
    length = 15
    excluded = ()
    if policy is not None:
        if policy["require_special"]:
            raise SystemExit("Password policy requires an unsupported composition rule.")
        length = policy["min_length"]
        excluded = policy["exclude_special"]

    allowed = string.ascii_letters + string.digits
    allowed += "".join(char for char in string.punctuation if char not in excluded)
    alphabet = allowed.encode("ascii")
    return bytearray(secrets.choice(alphabet) for _ in range(length))


def generate_unbreached_password(
    policy: dict | None, check: Callable[[bytearray], str]
) -> str | None:
    """Return display text for a verified candidate, or None if none passes.

    Wipe each mutable candidate, including the accepted candidate after decoding.
    The CLI owns the lifetime of the returned display text.
    """
    for _ in range(10):
        candidate = generate_password(policy)
        try:
            result = check(candidate)
            if result == "NOT_FOUND":
                return candidate.decode("ascii")
            if result != "BREACHED":
                return None
        finally:
            wipe_password(candidate)

    return None
