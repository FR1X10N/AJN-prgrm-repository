#!/usr/bin/python3
"""Process-level protections that run once at program start.

Owner: Ali Canli
"""

import os
import sys


def refuse_if_elevated():
    """Exit if the program runs with root or administrator privileges.

    A password tool does not need elevated rights. Running it as root or
    administrator would only increase the damage if something goes wrong.
    """
    if os.name == "nt":
        try:
            import ctypes

            is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError):
            # If the check itself is unavailable, do not block the user.
            is_admin = False
    else:
        is_admin = hasattr(os, "geteuid") and os.geteuid() == 0

    if is_admin:
        raise SystemExit(
            "Please do not run this program as root or administrator."
        )


def disable_core_dumps():
    """Set the core-dump limit to zero (Unix only).

    A core dump is a copy of the process memory written to disk after a
    crash. It could contain the password, so we switch it off.

    Returns True if core dumps were disabled, False if this is not
    supported (for example on Windows, where the resource module is missing).
    """
    try:
        import resource
    except ImportError:
        return False

    try:
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ValueError, OSError):
        return False

    return True


if __name__ == "__main__":
    refuse_if_elevated()
    print("Core dumps disabled:", disable_core_dumps(), file=sys.stderr)
