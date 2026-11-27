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
    excluded = set()
    require_special = False

    if policy is not None:
        length = secrets.randbelow(
            policy["max_length"] - policy["min_length"] + 1
        ) + policy["min_length"]
        excluded = set(policy["exclude_special"])
        require_special = policy["require_special"]

    letters_and_digits = string.ascii_letters + string.digits
    allowed_specials = "".join(
        char for char in string.punctuation if char not in excluded
    )
    allowed = letters_and_digits + allowed_specials

    if not allowed:
        raise ValueError("The password character set must not be empty.")

    if require_special:
        if not allowed_specials:
            raise ValueError(
                "The policy requires a special character, but none are allowed."
            )

        # Choose one required special character, then fill the remaining
        # positions from the full allowed alphabet.
        characters = [secrets.choice(allowed_specials)]
        characters.extend(
            secrets.choice(allowed) for _ in range(length - 1)
        )
        secrets.SystemRandom().shuffle(characters)
    else:
        characters = [
            secrets.choice(allowed) for _ in range(length)
        ]

    return bytearray("".join(characters), "ascii")


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
            result = check(candidate) # We need to distinguish `UNKNOWN` from `NOT_FOUND`: `NOT_FOUND` means the check succeeded and no breach was found, while `UNKNOWN` means the password could not be checked.
            if result == "NOT_FOUND":
                return candidate.decode("ascii")
            if result != "BREACHED":
                return None
        finally:
            wipe_password(candidate)

    return None
