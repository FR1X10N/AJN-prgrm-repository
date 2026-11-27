"""Unit tests for Nolan's password and HIBP modules."""

import getpass
import string
import http.client
import sys
import unittest
import warnings
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import api_client
import breach_check
import password


class PasswordTests(unittest.TestCase):
    def test_hidden_input_returns_utf8(self):
        with patch("password.getpass.getpass", return_value="Synthétique") as read:
            self.assertEqual(password.read_password("Prompt: "), bytearray("Synthétique", "utf-8"))
        read.assert_called_once_with("Prompt: ")

    def test_getpass_warning_stops_before_fallback(self):
        def fallback(prompt):
            warnings.warn("Echo unavailable", getpass.GetPassWarning)
            self.fail("Visible input fallback was reached")

        with patch("password.getpass.getpass", side_effect=fallback):
            with self.assertRaisesRegex(SystemExit, "securely"):
                password.read_password()

    def test_hash_and_wipe(self):
        buffer = bytearray(b"abc")
        self.assertEqual(
            password.hash_and_split_password(buffer),
            ("A9993", "E364706816ABA3E25717850C26C9CD0D89D"),
        )
        self.assertEqual(buffer, b"abc")
        password.wipe_password(buffer)
        self.assertEqual(buffer, b"\0" * 3)

    def test_generation_respects_policy(self):
        policy = {"min_length": 12, "max_length": 12,
                  "require_special": False, "exclude_special": ["!"]}
        with patch("password.secrets.choice", side_effect=lambda alphabet: alphabet[-1]) as choice:
            self.assertEqual(len(password.generate_password(None)), 15)
            self.assertIn("!", choice.call_args.args[0])
            self.assertEqual(len(password.generate_password(policy)), 12)
            self.assertNotIn("!", choice.call_args.args[0])

        # require_special is supported: the result contains an allowed special
        # character and never an excluded one.
        special_policy = dict(policy, require_special=True)
        for _ in range(50):
            candidate = password.generate_password(special_policy).decode("ascii")
            self.assertEqual(len(candidate), 12)
            self.assertTrue(any(char in string.punctuation for char in candidate))
            self.assertNotIn("!", candidate)

    def test_generation_stops_and_wipes_candidates(self):
        cases = (
            (["BREACHED", "NOT_FOUND"], "test", 2),
            (["UNKNOWN"], None, 1),
            (["BREACHED"] * 10, None, 10),
        )
        for results, expected, attempts in cases:
            with self.subTest(results=results):
                candidates = [bytearray(b"test") for _ in range(attempts)]
                check = Mock(side_effect=results)
                with patch("password.generate_password", side_effect=candidates):
                    self.assertEqual(password.generate_unbreached_password(None, check), expected)
                self.assertEqual(check.call_count, attempts)
                self.assertEqual(candidates, [bytearray(4) for _ in range(attempts)])

    def test_generation_wipes_after_checker_exception(self):
        candidate = bytearray(b"test")
        with patch("password.generate_password", return_value=candidate):
            with self.assertRaises(RuntimeError):
                password.generate_unbreached_password(None, Mock(side_effect=RuntimeError))
        self.assertEqual(candidate, bytearray(4))


class ApiClientTests(unittest.TestCase):
    def setUp(self):
        connector = patch("api_client.http.client.HTTPSConnection")
        self.connect = connector.start()
        self.addCleanup(connector.stop)
        self.connection = self.connect.return_value
        self.response = self.connection.getresponse.return_value
        self.response.status = 200
        self.response.length = 0
        self.body = b"A" * 35 + b":0\r\n"
        self.response.read.return_value = self.body

    def test_request_sends_only_prefix_with_padding(self):
        self.assertEqual(api_client.query_breach_api("abc12"), self.body.decode("ascii"))
        self.connect.assert_called_once_with("api.pwnedpasswords.com", timeout=5)
        self.connection.request.assert_called_once_with(
            "GET", "/range/ABC12",
            headers={"Add-Padding": "true", "User-Agent": "AJN-pwned.py"},
        )
        self.connection.close.assert_called_once()

    def test_invalid_prefix_never_connects(self):
        for prefix in ("ABC", "GH012", "AB12/", "A" * 40):
            self.assertIsNone(api_client.query_breach_api(prefix))
        self.connect.assert_not_called()

    def test_non_200_status_including_redirect(self):
        for status in (302, 404, 429, 503):
            self.response.status = status
            self.assertIsNone(api_client.query_breach_api("ABC12"))
        self.response.read.assert_not_called()

    def test_bad_response_or_transport_error(self):
        for body in (b"", b"\xff", b"<html>", self.body * 2, b"A" * (256 * 1024 + 1)):
            self.response.read.return_value = body
            self.assertIsNone(api_client.query_breach_api("ABC12"))

        self.response.read.return_value = self.body
        self.response.length = 10
        self.assertIsNone(api_client.query_breach_api("ABC12"))
        for error in (TimeoutError, OSError, http.client.IncompleteRead(b"")):
            self.response.read.side_effect = error
            self.assertIsNone(api_client.query_breach_api("ABC12"))


class BreachCheckTests(unittest.TestCase):
    def setUp(self):
        self.storage = SimpleNamespace(
            save_api_response=Mock(),
            check_suffix_in_response=Mock(),
            delete_api_response=Mock(),
        )
        modules = patch.dict(sys.modules, {"storage": self.storage})
        modules.start()
        self.addCleanup(modules.stop)
        api = patch("breach_check.query_breach_api", return_value="A" * 35 + ":0")
        self.query = api.start()
        self.addCleanup(api.stop)
        self.buffer = bytearray(b"abc")
        self.prefix, self.suffix = password.hash_and_split_password(self.buffer)

    def test_statuses_and_cleanup(self):
        for status in ("BREACHED", "NOT_FOUND", "UNKNOWN"):
            with self.subTest(status=status):
                self.storage.check_suffix_in_response.return_value = status
                self.storage.save_api_response.side_effect = (
                    lambda response, path: path.write_text(response, encoding="ascii")
                )
                self.storage.delete_api_response.side_effect = Path.unlink
                self.assertEqual(breach_check.check_password_once(self.buffer), status)
                self.query.assert_called_with(self.prefix)
                response, path = self.storage.save_api_response.call_args.args
                self.assertEqual(response, self.query.return_value)
                self.storage.check_suffix_in_response.assert_called_with(self.suffix, path)
                self.storage.delete_api_response.assert_called_with(path)
                self.assertFalse(path.parent.exists())
                self.assertEqual(self.buffer, b"abc")

    def test_api_failure_skips_storage(self):
        self.query.return_value = None
        self.assertEqual(breach_check.check_password_once(self.buffer), "UNKNOWN")
        self.storage.save_api_response.assert_not_called()

    def test_storage_errors_fail_closed_and_delete(self):
        for stage in ("save_api_response", "check_suffix_in_response", "delete_api_response"):
            with self.subTest(stage=stage):
                self.storage.check_suffix_in_response.return_value = "NOT_FOUND"
                failing = getattr(self.storage, stage)
                failing.side_effect = OSError
                self.storage.delete_api_response.reset_mock()
                self.assertEqual(breach_check.check_password_once(self.buffer), "UNKNOWN")
                path = self.storage.save_api_response.call_args.args[1]
                self.storage.delete_api_response.assert_called_once_with(path)
                self.assertFalse(path.parent.exists())
                failing.side_effect = None


if __name__ == "__main__":
    unittest.main()
