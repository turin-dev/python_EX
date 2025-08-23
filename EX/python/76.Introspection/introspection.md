# 제76장 – `inspect`를 통한 고급 인트로스펙션

`inspect` 모듈은 모듈, 클래스, 메서드, 함수, 코드 객체와 같은 라이브 객체를 검사하는 함수를 제공합니다【319197758890060†L65-L74】. 이 모듈을 사용하면 호출 가능한 객체의 시그니처, 소스 코드, 문서 문자열, 정의된 파일과 멤버를 검색할 수 있습니다. 인트로스펙션은 디버깅, 문서 생성, 사용자 코드에 대한 프레임워크 구현에 유용합니다.

## 호출 가능한 객체 검사

* `inspect.signature(callable)`은 해당 호출 가능 객체의 매개변수, 기본값, 어노테이션을 설명하는 `Signature` 객체를 반환합니다.
* `inspect.getsource(object)`는 객체의 소스 코드 텍스트를 반환합니다(가능한 경우).
* `inspect.getdoc(object)`는 객체의 문서 문자열을 반환합니다.

```python
import inspect

def greet(name: str, times: int = 1) -> None:
    """Print a greeting multiple times."""
    for _ in range(times):
        print("Hello,", name)

sig = inspect.signature(greet)
print("Signature:", sig)
print("Docstring:", inspect.getdoc(greet))
print("Source:\n", inspect.getsource(greet))
```

## 클래스와 모듈 검사

`inspect.getmembers()`는 객체의 멤버 이름과 객체의 쌍 목록을 반환합니다. `inspect.isfunction`이나 `inspect.isclass`와 같은 술어와 결합하여 특정 유형의 멤버를 필터링할 수 있습니다. `inspect.getmodule(object)`는 객체가 정의된 모듈을 찾습니다.

```python
import inspect
import math

members = inspect.getmembers(math, inspect.isbuiltin)
print("Built‑in functions in math:", [name for name, obj in members])
```

## 요약

`inspect` 모듈을 사용하면 호출 가능한 객체의 서명, 소스 코드, 문서 및 멤버를 얻을 수 있습니다. 이러한 기능을 이용하면 함수에 대한 정보를 추출하여 자동 API를 구축하거나 소스에서 문서를 생성하는 등의 작업을 할 수 있습니다【319197758890060†L65-L74】.