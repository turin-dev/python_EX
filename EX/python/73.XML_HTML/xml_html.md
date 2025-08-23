# 제73장 – XML과 HTML 파싱

파이썬은 XML과 HTML을 분석하고 생성하기 위한 모듈을 포함하고 있습니다. `xml.etree.ElementTree` 모듈은 XML 문서를 위한 가벼운 DOM과 유사한 인터페이스를 제공하며, `html.parser` 모듈은 HTML을 이벤트 기반으로 파싱하는 클래스의 구현을 제공합니다. 이러한 파서는 텍스트 문자열과 파일 객체에서 작동하며, 파일 I/O는 플랫폼 간에 동일한 API를 사용한다는 점을 기억하세요【549557713116431†L69-L76】.

## ElementTree로 XML 처리

`xml.etree.ElementTree`는 XML을 `Element` 객체의 트리로 파싱합니다. `fromstring()`이나 `parse()`를 사용해 트리를 생성하고, 태그와 속성을 통해 탐색합니다. 또한 XML 문서를 구축하고 `ElementTree.write()`로 파일에 저장할 수 있습니다.

```python
import xml.etree.ElementTree as ET

xml_data = """
<catalog>
  <book id="bk101">
    <title>XML Developer's Guide</title>
    <price>44.95</price>
  </book>
</catalog>
"""

root = ET.fromstring(xml_data)
for book in root.findall('book'):
    title = book.find('title').text
    price = float(book.find('price').text)
    print(title, price)
```

## HTML 파싱

`html.parser` 모듈은 이벤트 기반 HTML 파싱을 위한 `HTMLParser` 기본 클래스를 정의합니다. 이 클래스를 상속하고 `handle_starttag`, `handle_endtag`, `handle_data` 메서드를 재정의하여 HTML 콘텐츠를 처리할 수 있습니다. 단순히 태그에서 텍스트를 추출하는 등의 작업에는 `html.parser`를 직접 사용하거나 BeautifulSoup과 같은 서드파티 라이브러리를 사용할 수 있습니다.

```python
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
    def handle_data(self, data):
        print("Data:", data)

parser = MyHTMLParser()
parser.feed("<html><body><h1>Hello!</h1></body></html>")
```

## 요약

XML을 파싱하고 생성하려면 `xml.etree.ElementTree`를 사용하고, 간단한 HTML 파싱 작업에는 `html.parser`를 사용하세요. 두 모듈 모두 문자열이나 파일 객체와 함께 작동하며, 파이썬의 휴대성 있는 파일 I/O API를 활용합니다【549557713116431†L69-L76】.