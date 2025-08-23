"""예제 23: asyncio를 이용한 비동기 프로그래밍.

이 파일은 간단한 비동기 코루틴과 태스크를 정의하고, 여러 작업을 동시에 실행하는
방법을 보여 준다. 외부 라이브러리 없이도 비동기 sleep을 사용하여 동작을
시뮬레이션한다.
"""

import asyncio
from datetime import datetime


async def print_with_timestamp(msg: str, delay: float) -> None:
    """주어진 지연 후 현재 시간을 출력하고 메시지를 반환한다."""
    await asyncio.sleep(delay)
    print(f"{datetime.now():%H:%M:%S} - {msg}")


async def run_tasks() -> None:
    """두 개의 코루틴을 동시에 실행한다."""
    task1 = asyncio.create_task(print_with_timestamp("First coroutine", 1.5))
    task2 = asyncio.create_task(print_with_timestamp("Second coroutine", 2.0))
    await asyncio.gather(task1, task2)
    print("Both coroutines completed.")


async def main() -> None:
    """메인 엔트리 포인트: 비동기 작업을 실행한다."""
    await run_tasks()
    # 동기 함수를 별도의 스레드에서 실행 (Python 3.9+)
    result = await asyncio.to_thread(sum, range(1_000_000))
    print("Sum of 1..999999:", result)


if __name__ == '__main__':
    asyncio.run(main())