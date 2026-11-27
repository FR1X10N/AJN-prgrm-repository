#!/usr/bin/python3
"""Temporary storage of the API response as a JSON file.

Owner: Ali Canli

The HIBP range API answers with plain text, one line per hash suffix:

    0018A45C4D1DEF81644B54AB7F969B88D65:10
    00D4F6E8FA6EECAD2A3AA415EEC418D38EC:0

save_api_response() turns this into a JSON object {"SUFFIX": count, ...}
and writes it with owner-only permissions. Entries with count 0 are padding
added by the API (Add-Padding header) and do not mean "breached".

This module makes no API requests and never sees the password.
"""

import json
import os

BREACHED = "BREACHED"
NOT_FOUND = "NOT_FOUND"
UNKNOWN = "UNKNOWN"

SUFFIX_LENGTH = 35
_HEX = set("0123456789ABCDEF")


def _parse_response(response):
    """Convert the API text into a dict {suffix: count}.

    Raises ValueError if the text does not look like a range API response.
    """
    if isinstance(response, (bytes, bytearray)):
        response = response.decode("utf-8")
    if not isinstance(response, str):
        raise ValueError("The API response must be text.")

    entries = {}
    for line in response.splitlines():
        line = line.strip()
        if not line:
            continue
        suffix, separator, count = line.partition(":")
        suffix = suffix.upper()
        if (
            separator != ":"
            or len(suffix) != SUFFIX_LENGTH
            or not set(suffix) <= _HEX
            or not count.isdigit()
        ):
            raise ValueError("The API response has an unexpected format.")
        entries[suffix] = int(count)

    if not entries:
        raise ValueError("The API response is empty.")
    return entries


def save_api_response(response, path):
    """Save the API's text list as a JSON file with owner-only permissions.

    Raises ValueError for a malformed response and OSError if the file
    cannot be written. The caller (check_password_once) turns both into
    the result UNKNOWN.
    """
    entries = _parse_response(response)

    # Create the file with permissions 0600 (only the owner can read/write).
    # On Windows the mode is mostly ignored; the file then lives in the
    # user's own temp folder.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as file:
        json.dump(entries, file)
    if os.name != "nt":
        os.chmod(path, 0o600)  # in case the file already existed


def check_suffix_in_response(suffix, path):
    """Look up the suffix in the saved JSON.

    Returns "BREACHED", "NOT_FOUND", or "UNKNOWN" (if the file is missing,
    unreadable, or not in the expected format).
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            entries = json.load(file)
    except (OSError, ValueError):
        return UNKNOWN

    if not isinstance(entries, dict) or not entries:
        return UNKNOWN

    if not isinstance(suffix, str):
        return UNKNOWN
    count = entries.get(suffix.upper(), 0)
    if type(count) is not int or count < 0:
        return UNKNOWN

    return BREACHED if count > 0 else NOT_FOUND


def delete_api_response(path):
    """Delete the temporary JSON file. Does nothing if it is already gone."""
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
