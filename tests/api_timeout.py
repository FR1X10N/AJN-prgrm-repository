#!/usr/bin/python3
import http.client
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import api_client
from cli import report_result


class TestTimeoutUserMessage(unittest.TestCase):
    @patch(
        "http.client.HTTPSConnection",
        side_effect=TimeoutError("request timed out"),
    )
    def test_timeout_is_detected_and_user_message_is_displayed(
        self, mock_connection
    ):
        # Der API-Client muss den Timeout in die spezifische Exception umwandeln.
        with self.assertRaises(api_client.APITimeoutError):
            api_client.query_breach_api("ABCDE")

        # Die CLI muss für den entsprechenden Status eine Meldung ausgeben.
        output = io.StringIO()
        with redirect_stdout(output):
            report_result("API_TIMEOUT")
        
        print(output.getvalue(), end="")

        self.assertEqual(
            output.getvalue().strip(),
            "The API request timed out.",
        )


if __name__ == "__main__":
    unittest.main()
