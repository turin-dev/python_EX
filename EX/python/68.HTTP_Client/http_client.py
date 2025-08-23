"""Examples using urllib.request and urllib.parse."""

from __future__ import annotations

from urllib.request import urlopen, Request
from urllib.parse import urlparse, urlencode, urlunparse


def fetch_url(url: str) -> int:
    """Fetch a URL and return the length of its content."""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req) as response:
        data = response.read()
        return len(data)


def build_search_url(query: str, page: int) -> str:
    """Construct a simple search URL with query parameters."""
    params = urlencode({"q": query, "page": page})
    return urlunparse(("https", "example.com", "/search", "", params, ""))


if __name__ == "__main__":
    # Only run if network is reachable (may fail in offline environment)
    try:
        length = fetch_url("https://www.python.org")
        print("Fetched bytes:", length)
    except Exception as e:
        print("Could not fetch URL:", e)
    url = build_search_url("python", 1)
    print("Constructed search URL:", url)