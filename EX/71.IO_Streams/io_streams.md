# 제71장 – `io`를 활용한 메모리 내 스트림

디스크의 파일을 읽고 쓰는 것 외에도 파이썬은 `io` 모듈을 통해 메모리 내 스트림 클래스를 제공합니다. 이러한 스트림은 파일 객체처럼 동작하지만 데이터를 메모리에 저장합니다. 파일 시스템을 사용하지 않고 텍스트나 바이너리 데이터를 조작할 때 유용하며, 파일과 유사한 객체를 기대하는 API에 전달할 수 있습니다. `read()`, `write()`, `seek()` 등의 메서드는 디스크 파일과 메모리 스트림에서 동일하게 작동합니다【549557713116431†L69-L76】.

## 텍스트와 바이너리 스트림

* **`io.StringIO`** – 메모리 내 텍스트 스트림입니다. `str` 객체를 받아들이고 반환하며, 표준 텍스트 파일 메서드를 모두 지원합니다. 큰 문자열을 효율적으로 조합하거나 수정할 때 사용하세요.
* **`io.BytesIO`** – 메모리 내 바이너리 스트림입니다. `bytes` 객체를 받아들이고 반환합니다. 바이너리 메시지를 구성하거나 파일과 유사한 객체를 기대하는 API에 전달할 때 사용합니다.

```python
from io import StringIO, BytesIO

text_buffer = StringIO()
text_buffer.write("Hello, ")
text_buffer.write("world!")
print(text_buffer.getvalue())  # 'Hello, world!'

binary_buffer = BytesIO()
binary_buffer.write(b"\x00\x01\x02")
binary_buffer.seek(0)
print(binary_buffer.read())  # b'\x00\x01\x02'
```

## 파일과 유사한 인터페이스

많은 API는 `read()`와 `write()` 메서드를 구현한 객체를 받아들입니다. `StringIO`와 `BytesIO`를 사용하면 파일에 쓰여야 하는 출력물을 가로채거나, 파일에서 읽는 함수에 메모리상의 데이터를 제공할 수 있습니다. 사용이 끝나면 `.close()`를 호출하여 리소스를 해제하세요.

## 요약

`io.StringIO`와 `io.BytesIO`를 사용하면 완전히 메모리 내에서 동작하는 파일과 유사한 객체를 만들 수 있습니다. 이들은 파일 객체와 동일한 인터페이스를 제공하므로 파일 핸들을 기대하는 코드를 수정하지 않고도 메모리 기반 처리를 수행할 수 있습니다【549557713116431†L69-L76】.