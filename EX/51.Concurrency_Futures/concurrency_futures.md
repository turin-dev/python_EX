# 51장 – `concurrent.futures`를 사용한 비동기 실행

파이썬의 `concurrent.futures` 모듈은 스레드 풀과 프로세스 풀을 이용해 함수를 비동기적으로 실행할 수 있는 간단한 고수준 API를 제공한다. 이 모듈은 작업자 스레드나 프로세스를 생성하고 관리하는 복잡함을 숨기고, 작업을 제출하고 결과를 수집하는 데 집중할 수 있게 해준다. 두 풀은 공통된 `Executor` 인터페이스를 구현하며, 완료되지 않은 계산을 나타내는 `Future` 객체를 반환한다. 공식 문서는 비동기 실행을 스레드 또는 별도 프로세스로 수행할 수 있고, 두 executor 모두 작업을 예약하는 `submit()`과 `map()` 메서드를 제공한다고 설명한다【910805816462369†L66-L119】.

## 핵심 개념

* **Executor** – `Executor`의 구체적인 하위 클래스는 작업자 풀을 관리한다. `ThreadPoolExecutor`는 백그라운드 스레드를 사용하고, `ProcessPoolExecutor`는 `multiprocessing` 모듈을 이용해 워커 프로세스를 생성한다. 프로세스 풀은 GIL(Global Interpreter Lock)을 우회하므로 CPU 바운드 코드를 병렬로 실행할 수 있지만, 제출되는 호출 가능 객체와 인수는 직렬화(pickle) 가능해야 한다【910805816462369†L66-L119】.
* **Future** – `Future` 객체는 진행 중이거나 완료된 계산을 나타낸다. `executor.submit(func, *args, **kwargs)`를 호출하면 즉시 future가 반환되고, 워커에서 함수를 실행하여 결과나 예외를 저장한다. future의 상태를 확인하거나 `result()`로 완료될 때까지 기다리거나, 콜백을 연결할 수 있다.
* **map 작업** – `Executor.map(func, iterable, timeout=None, chunksize=1)`은 반복 가능한 모든 항목에 대해 함수를 실행하도록 예약한다. 프로세스 풀에서는 반복 가능한 객체가 즉시 소비되고, 프로세스 간 통신 오버헤드를 줄이기 위해 청크 단위로 나뉠 수 있다【910805816462369†L93-L119】.
* **리소스 관리** – Executor는 컨텍스트 매니저를 구현한다. `with ThreadPoolExecutor() as executor:` 형태로 사용하면 스레드/프로세스가 적절히 정리된다. 컨텍스트 매니저를 사용하지 않을 경우 `executor.shutdown()`을 직접 호출해야 한다.

## 예제: 병렬로 작업 실행하기

다음 예제는 스레드 풀을 사용해 여러 URL을 동시에 다운로드하는 방법을 보여준다. 각 호출은 응답 본문의 길이를 반환한다. 프로세스 풀도 비슷하게 동작하지만, CPU 바운드 작업에 더 적합하다.

```python
from concurrent.futures import ThreadPoolExecutor
import urllib.request

def fetch(url: str) -> int:
    """Download content and return its size."""
    with urllib.request.urlopen(url) as response:
        return len(response.read())

urls = [
    "https://example.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
]

# 컨텍스트 매니저를 사용해 스레드를 정리한다
with ThreadPoolExecutor(max_workers=3) as executor:
    # 작업을 제출하고 future를 수집한다
    futures = [executor.submit(fetch, url) for url in urls]
    for future in futures:
        size = future.result()  # 각 future가 완료되기를 기다리고 결과를 가져온다
        print(f"Downloaded {size} bytes")
```

## 요약

`concurrent.futures`는 서로 독립적인 작업을 손쉽게 병렬화할 수 있게 해준다. 블로킹 I/O로 인해 스레드가 대기하는 **I/O 바운드** 작업에는 `ThreadPoolExecutor`를, 여러 코어를 활용하면 성능이 향상되는 **CPU 바운드** 작업에는 `ProcessPoolExecutor`를 사용하라. `Future`는 비동기 결과를 캡슐화하여 작업 완료를 깔끔하게 조정할 수 있게 한다【910805816462369†L66-L119】.