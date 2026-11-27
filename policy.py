#!/usr/bin/python3


import json
import string
from pathlib import Path


def load_policy(args):
    """Return the active policy, or None in User Mode."""
    if not args.company_mode:
        return None

    policy_path = Path(args.policy)

    try:
        with policy_path.open("r", encoding="utf-8") as file:
            policy = json.load(file)
    except (OSError, ValueError) as exc:
        # ValueError covers JSONDecodeError and UnicodeDecodeError.
        raise SystemExit(f"Invalid policy file: {exc}")

    required_keys = {
        "min_length",
        "max_length",
        "require_special",
        "exclude_special",
    }

    if not isinstance(policy, dict) or set(policy) != required_keys:
        raise SystemExit(
            "Invalid policy: expected exactly these fields: "
            "min_length, max_length, require_special, and exclude_special."
        )

    min_length = policy["min_length"]
    max_length = policy["max_length"]
    require_special = policy["require_special"]
    exclude_special = policy["exclude_special"]

    # In Python, bool is a subclass of int, so check the types explicitly.
    if type(min_length) is not int or type(max_length) is not int:
        raise SystemExit("min_length and max_length must be integers.")
    if min_length < 1 or max_length < min_length:
        raise SystemExit(
            "Password lengths must be valid: 1 <= min_length <= max_length."
        )
    if type(require_special) is not bool:
        raise SystemExit("require_special must be true or false.")
    if not isinstance(exclude_special, list) or not all(
        isinstance(char, str) and len(char) == 1 for char in exclude_special
    ):
        raise SystemExit(
            "exclude_special must be a list containing single characters."
        )

    allowed_specials = set(string.punctuation) - set(exclude_special)
    if require_special and not allowed_specials:
        raise SystemExit(
            "Invalid policy: require_special is true, but all special characters "
            "are excluded."
        )

    return policy


def validate_password_policy(password, policy):
    """Return True if the password complies with the policy."""
    if policy is None:
        return True

    if not isinstance(password, str):
        return False

    if not policy["min_length"] <= len(password) <= policy["max_length"]:
        return False

    excluded_specials = set(policy["exclude_special"])
    password_specials = {
        char for char in password
        if char in string.punctuation
    }

    if password_specials & excluded_specials:
        return False

    if policy["require_special"]:
        allowed_specials = set(string.punctuation) - excluded_specials
        if not password_specials & allowed_specials:
            return False

    return True
