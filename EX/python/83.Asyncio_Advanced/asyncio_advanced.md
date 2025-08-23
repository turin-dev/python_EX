# 제83장 – `asyncio`를 활용한 고급 비동기 프로그래밍

파이썬의 `asyncio` 라이브러리는 `async`/`await` 구문을 사용하여 동시성을 구현할 수 있게 합니다. 이벤트 루프, 태스크, 코루틴을 제공하여 비동기 작업을 관리하며, I/O 바운드 코드에 적합합니다【514012888195974†L62-L69】. 기본 개념을 넘어, `asyncio`는 스트림 API, 동기화 프리미티브, 서브프로세스 관리 등 고급 기능을 지원합니다.

## 스트림 API

`asyncio`는 비동기 I/O를 위해 `StreamReader`와 `StreamWriter` 객체를 제공합니다. `asyncio.open_connection(host, port)`를 호출하면 TCP 연결을 열고 리더/라이터 객체를 반환합니다. `await reader.read(n)`과 `writer.write(data)`를 사용해 블로킹 없이 읽고 쓸 수 있습니다.

```python
import asyncio

async def echo_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(b"Hello\n")
    await writer.drain()
    data = await reader.readline()
    print("Received:", data.decode())
    writer.close()
    await writer.wait_closed()

asyncio.run(echo_client("localhost", 8000))
```

## 동기화 프리미티브

`threading` 모듈과 유사하게, `asyncio`는 `Lock`, `Event`, `Condition`, `Semaphore` 클래스를 제공합니다. 이러한 프리미티브를 사용하면 코루틴 간 협력을 관리할 수 있습니다. 또한 `asyncio.Queue`는 프로듀서/컨슈머 패턴을 지원하는 코루틴 친화적 큐입니다.

## 서브프로세스 생성

`asyncio.create_subprocess_exec()` 또는 `create_subprocess_shell()`을 사용하여 서브프로세스를 비동기적으로 생성할 수 있습니다. 반환되는 `Process` 객체에는 읽기/쓰기 및 완료를 기다리기 위한 코루틴 메서드가 있습니다.

## 요약

`asyncio`는 스트림 API, 동기화 프리미티브, 서브프로세스 관리 등 기본 코루틴을 넘어선 기능을 제공합니다【514012888195974†L62-L69】. 이러한 기능을 이용해 네트워크 클라이언트/서버를 구현하고, 여러 코루틴을 조정하며, 이벤트 루프를 차단하지 않고 외부 명령을 실행할 수 있습니다.