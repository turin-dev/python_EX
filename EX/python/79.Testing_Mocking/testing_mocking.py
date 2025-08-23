"""Unit testing and mocking examples using unittest and unittest.mock."""

from __future__ import annotations

import unittest
from unittest.mock import patch


def greet(name: str) -> str:
    return f"Hello, {name}!"


class GreetTest(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(greet("Alice"), "Hello, Alice!")
    def test_subtests(self) -> None:
        names = ["Bob", "Carol", "Dave"]
        for n in names:
            with self.subTest(name=n):
                self.assertTrue(greet(n).startswith("Hello"))


def fetch_data(url: str) -> str:
    import urllib.request
    with urllib.request.urlopen(url) as f:
        return f.read().decode()


class FetchDataTest(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def test_fetch_data(self, mock_urlopen):
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value = b"Mock Data"
        result = fetch_data("http://example.com")
        self.assertEqual(result, "Mock Data")
        mock_urlopen.assert_called_once()


if __name__ == "__main__":
    unittest.main()