# 제68장 – HTTP 클라이언트와 URL 처리

파이썬의 `urllib` 패키지는 URL과 HTTP 처리를 위한 모듈을 제공합니다. `urllib.request`는 웹 리소스를 가져오고, `urllib.parse`는 URL 문자열을 분해하고 다시 구성하며, `urllib.error`는 예외를 처리합니다. 이러한 모듈은 내부적으로 소켓을 사용하여 네트워크 I/O를 수행합니다【634526119538162†L67-L86】.

## `urllib.request`로 데이터 가져오기

`urlopen()` 함수는 주어진 URL의 리소스를 위해 파일과 유사한 객체를 반환합니다. 헤더, 요청 메서드, 시간 제한 등을 지정하려면 `Request` 객체를 생성하여 사용합니다. 응답 본문은 `read()`로 읽을 수 있습니다.

```python
from urllib.request import urlopen, Request

req = Request("https://www.python.org", headers={"User-Agent": "Mozilla/5.0"})
with urlopen(req) as response:
    html = response.read()
    print("Retrieved", len(html), "bytes")
```

HTTP 오류와 네트워크 오류는 각각 `urllib.error.HTTPError`와 `urllib.error.URLError`로 처리할 수 있습니다.

## URL 파싱과 생성

`urllib.parse`는 URL을 구성 요소로 분해하기 위한 `urlparse()`와 `urlsplit()` 함수를 제공합니다. 또한 쿼리 문자열을 생성하고 상대 경로를 기준 URL에 결합하는 함수도 제공합니다.

```python
from urllib.parse import urlparse, urlencode, urlunparse

url = "https://example.com/index.html?query=python#section"
parts = urlparse(url)
print(parts.scheme, parts.netloc, parts.path)

# 쿼리 매개변수를 사용해 URL 만들기
params = {"q": "urllib", "page": 2}
query_str = urlencode(params)
new_url = urlunparse(("https", "example.com", "/search", "", query_str, ""))
print(new_url)
```

## 요약

`urllib.request`를 사용하여 웹 리소스를 가져오고 리다이렉트나 오류를 처리하세요. `urllib.parse`는 URL을 분해하거나 쿼리 매개변수를 인코딩하는 데 유용하며, 퍼센트 인코딩을 자동으로 처리합니다. 이러한 모듈은 소켓 위에서 동작하는 경량 HTTP 클라이언트를 제공합니다【634526119538162†L67-L86】.