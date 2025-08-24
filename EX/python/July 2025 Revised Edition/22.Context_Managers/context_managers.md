# 22. 컨텍스트 매니저와 `with` 문

파일이나 네트워크 연결처럼 사용 후 반드시 정리해야 하는 자원을 다룰 때 **컨텍스트 매니저**를 사용하면 안전하고 간결하게 초기화와 해제를 처리할 수 있다. 파이썬은 `with` 문을 통해 컨텍스트 매니저를 지원하며, 이는 블록의 실행 전후에 초기화 및 정리 코드를 자동으로 실행한다【154098694026921†L89-L95】.

## `with` 문 기본 사용법

가장 흔한 예는 파일 입출력이다. 파일을 열면 컨텍스트 매니저가 반환되며, `with` 문을 빠져나올 때 파일이 자동으로 닫힌다.

```python
with open('example.txt', 'w', encoding='utf-8') as f:
    f.write('Hello world!')
```

`with` 문은 여러 컨텍스트 매니저를 동시에 사용할 수 있으며, 각 매니저는 순서대로 초기화되고 종료된다.

## 사용자 정의 컨텍스트 매니저 클래스

사용자 정의 객체를 `with` 문에서 사용하려면 `__enter__()`와 `__exit__()` 메서드를 구현해야 한다. `__enter__()`는 블록 시작 시 호출되어 자원을 준비하고, `__exit__()`는 블록이 종료될 때 호출되어 정리 작업을 수행한다.

```python
class ManagedFile:
    def __init__(self, filename: str):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, 'w', encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc, tb):
        if self.file:
            self.file.close()
        # 예외가 발생했을 경우 추가 처리 가능. 반환값이 True면 예외를 억제한다.
        return False

with ManagedFile('log.txt') as f:
    f.write('Logging via context manager')
```

## `contextlib` 모듈과 제너레이터 기반 매니저

파이썬의 `contextlib` 모듈은 데코레이터를 사용하여 간단하게 컨텍스트 매니저를 정의할 수 있는 `@contextmanager` 데코레이터를 제공한다【743908840044846†L93-L144】. 제너레이터 함수에서 `yield` 앞은 `__enter__()`의 코드, `yield` 뒤는 `__exit__()`에 해당한다.

```python
from contextlib import contextmanager

@contextmanager
def open_uppercase(path: str):
    f = open(path, 'r', encoding='utf-8')
    try:
        # 엔터 시 파일 객체를 반환
        yield (line.upper() for line in f)
    finally:
        # 예외 여부와 상관없이 항상 실행
        f.close()

with open_uppercase('message.txt') as lines:
    for line in lines:
        print(line)
```

`@contextmanager`를 사용하면 복잡한 클래스 정의 없이도 간단히 컨텍스트 매니저를 구현할 수 있다【743908840044846†L93-L144】. 또한 `contextlib.ExitStack`을 통해 여러 매니저를 동적으로 조합할 수 있으며, 임시 리소스를 관리하는 `contextlib.redirect_stdout` 같은 유틸리티도 제공한다.

## `with` 문의 장점

- **자원 누수 방지**: 예외 발생 여부와 관계없이 자원이 적절히 해제된다.
- **가독성**: 초기화와 정리 코드가 명확하게 분리되어 코드 흐름을 이해하기 쉽다.
- **중첩 관리**: 여러 자원을 깔끔하게 중첩해서 사용할 수 있으며, `contextlib.ExitStack`으로 동적으로 관리할 수 있다.

컨텍스트 매니저를 활용하면 코드의 안정성과 유지보수성이 크게 향상된다.