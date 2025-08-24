# 23. 비동기 프로그래밍과 `asyncio`

**`asyncio`** 모듈은 비동기 I/O에 특화된 프레임워크로, *코루틴(coroutine)*과 *이벤트 루프*를 이용해 단일 스레드에서 많은 I/O 작업을 동시에 처리할 수 있게 한다. 공식 문서는 `asyncio`가 **`async`/`await` 문법을 사용해 비동기 코드 작성을 지원하며, 주로 네트워크나 I/O‑바운드 코드에 적합하다**고 설명한다【514012888195974†L62-L69】.

## 코루틴과 이벤트 루프

- **코루틴**은 `async def`로 정의된 함수로, 호출 시 바로 실행되지 않고 *코루틴 객체*를 반환한다.
- 코루틴 내부에서 `await` 키워드를 사용하면 다른 코루틴이나 비동기 함수의 완료를 기다리는 동안 이벤트 루프가 다른 작업을 실행할 수 있다.
- **이벤트 루프**는 준비된 코루틴을 스케줄링하고, I/O 이벤트가 완료되면 적절한 콜백을 실행한다. `asyncio.run()` 함수를 사용하면 이벤트 루프를 생성하고 주 코루틴을 실행한 뒤 종료한다.

## 기본 예제

아래 예제는 웹에서 데이터를 가져오는 비동기 함수와 여러 작업을 동시에 실행하는 방법을 보여준다. `asyncio` 모듈을 사용하면 단일 스레드에서도 네트워크 요청을 병렬로 처리할 수 있다.

```python
import asyncio
import aiohttp  # 서드파티 비동기 HTTP 클라이언트

async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    urls = [
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/posts/2',
        'https://jsonplaceholder.typicode.com/posts/3',
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_json(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for result in results:
            print(result['title'])

if __name__ == '__main__':
    asyncio.run(main())
```

## 태스크와 `asyncio.gather()`

`asyncio.create_task()`는 코루틴을 *태스크*로 스케줄링하여 병렬로 실행하게 한다. 여러 태스크를 동시에 기다리려면 `asyncio.gather()`를 사용한다. 태스크는 독립적으로 실행되므로 하나가 블록되어도 다른 작업이 진행된다.

```python
async def coroutine_a():
    print('Start A'); await asyncio.sleep(1); print('End A')

async def coroutine_b():
    print('Start B'); await asyncio.sleep(2); print('End B')

async def run_tasks():
    task1 = asyncio.create_task(coroutine_a())
    task2 = asyncio.create_task(coroutine_b())
    await asyncio.gather(task1, task2)

asyncio.run(run_tasks())
```

## 비동기 함수와 동기 코드의 조합

비동기 함수 안에서 동기 함수를 호출해야 한다면 `run_in_executor()`를 사용해 블로킹 코드를 별도 스레드나 프로세스로 실행할 수 있다. 또한 `asyncio.to_thread()`는 간단한 함수를 자동으로 스레드 풀에서 실행한다.

비동기 프로그래밍은 I/O‑바운드 작업의 효율을 크게 높여 주지만, CPU‑바운드 작업에는 `threading`이나 `multiprocessing`이 더 적합하다. 적절한 도구를 선택하는 것이 중요하다.