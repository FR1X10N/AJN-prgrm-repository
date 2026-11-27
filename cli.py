#!/usr/bin/python3

import process_security
from breach_check import check_password_once
from password import generate_unbreached_password, read_password
from policy import load_policy, validate_password_policy


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        description="Checks passwords and optionally supports Company Mode."
    )
    parser.add_argument(
        "--company-mode",
        action="store_true",
        help="Start the program in Company Mode.",
    )
    parser.add_argument(
        "--policy",
        metavar="FILE",
        help="Path to the policy JSON file (required in Company Mode).",
    )

    args = parser.parse_args()

    if args.company_mode and not args.policy:
        parser.error("--policy FILE is required in Company Mode.")
    if args.policy and not args.company_mode:
        parser.error("--policy can only be used together with --company-mode.")

    return args


def verify_password(password):
    """Check the password once, then clear its mutable buffer."""
    try:
        return check_password_once(password)
    finally:
        # Overwrite the password buffer, even if the check raises an exception.
        password[:] = b"\x00" * len(password)


def report_result(result):
    """Print the password check result in the terminal."""
    messages = {
        "BREACHED": "This password was found in known data breaches.",
        "NOT_FOUND": "No breach was found for this password.",
        "UNKNOWN": "The password could not be checked.",
    }

    print(messages.get(result, f"Unexpected result: {result}"))


def display_generated_password(password):
    """Display a generated password after the user confirms."""
    confirmation = input(
        "Display the generated password? [y/N] "
    ).strip().lower()

    if confirmation in {"y", "yes"}:
        print(f"Generated password: {password}")


def main():
    def main():
    process_security.refuse_if_elevated()
    process_security.disable_core_dumps()

    args = parse_arguments()
    policy = load_policy(args)

    while True:
        password = read_password("Enter a password: ")

        try:
            password_text = password.decode("utf-8")
        except UnicodeDecodeError:
            password[:] = b"\x00" * len(password)
            print("The password must be valid UTF-8. Please try again.")
            continue

        complies_with_policy = validate_password_policy(password_text, policy)

        # Check for breaches regardless of policy compliance.
        result = verify_password(password)
        report_result(result)

        if not complies_with_policy:
            print("The password does not comply with the active policy.")

        should_offer_generation = (
            not complies_with_policy or result == "BREACHED"
        )

        if should_offer_generation:
            if not complies_with_policy:
                prompt = "Would you like to generate a new password? [y/N] "
            else:
                prompt = (
                    "Would you like to generate an unbreached password? [y/N] "
                )

            confirmation = input(prompt).strip().lower()

            if confirmation in {"y", "yes"}:
                generated_password = generate_unbreached_password(
                    policy,
                    check_password_once,
                )

                if generated_password is None:
                    print("Could not generate a verified password.")
                else:
                    display_generated_password(generated_password)
        break
