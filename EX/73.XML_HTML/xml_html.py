"""Parsing XML and HTML using ElementTree and HTMLParser."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from html.parser import HTMLParser


def parse_xml() -> None:
    xml_data = """
    <root>
      <item name="alpha">1</item>
      <item name="beta">2</item>
    </root>
    """
    root = ET.fromstring(xml_data)
    for item in root.findall('item'):
        print(item.get('name'), item.text)


class TextExtractor(HTMLParser):
    """Extract and print data inside HTML tags."""
    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            print("Text:", text)


def parse_html() -> None:
    parser = TextExtractor()
    html = "<html><head><title>Sample</title></head><body><p>Hello <b>world</b>!</p></body></html>"
    parser.feed(html)


if __name__ == "__main__":
    parse_xml()
    parse_html()