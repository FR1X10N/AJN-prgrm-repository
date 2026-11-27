#!/usr/bin/python3
"""Central logging that never records passwords, hashes, or API contents.

Owner: Ali Canli

Only short, fixed status messages should be passed in, for example
"API request started" or "Temporary file deleted". As an extra safety net,
anything that looks like a SHA-1 hash or hash part is replaced before it is
written.
"""

import logging
import re

LOGGER_NAME = "pwned"

# Hex strings of 5 or more characters: covers the 5-char prefix,
# the 35-char suffix, and the full 40-char SHA-1 hash.
_HEX_PATTERN = re.compile(r"\b[0-9A-Fa-f]{5,}\b")

_logger = logging.getLogger(LOGGER_NAME)
# No output unless the program configures logging on purpose.
_logger.addHandler(logging.NullHandler())


def _redact(message):
    """Replace hash-like parts of a message with a placeholder."""
    return _HEX_PATTERN.sub("[redacted]", message)


def log_safe_event(message, level=logging.INFO):
    """Log a non-sensitive status message.

    Never pass the password, the hash, or the API response to this function.
    """
    if not isinstance(message, str):
        message = type(message).__name__
    _logger.log(level, _redact(message))
