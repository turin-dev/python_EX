# 24. 스레딩: I/O‑바운드 병렬 처리

`threading` 모듈은 Python 코드에서 여러 스레드를 사용해 I/O‑바운드 작업을 병렬로 처리할 수 있게 한다. 문서에서는 *여러 I/O‑연산을 동시에 실행할 때 유용하지만, 전역 인터프리터 잠금(Global Interpreter Lock, GIL) 때문에 한 번에 하나의 스레드만 바이트코드를 실행한다*고 명시한다【570737854010064†L77-L150】. 따라서 CPU‑집약적인 병렬화에는 `multiprocessing`이 적합하다.

## 스레드 생성과 실행

스레드는 `threading.Thread` 클래스를 사용하여 생성한다. 타겟 함수와 인자를 지정한 뒤 `start()`를 호출하면 스케줄러가 스레드를 실행한다. `join()` 메서드로 스레드가 끝날 때까지 기다릴 수 있다.

```python
import threading
import time

def count_down(n: int) -> None:
    while n > 0:
        print(f"Counting down: {n}")
        time.sleep(1)
        n -= 1

threads = []
for i in range(3):
    t = threading.Thread(target=count_down, args=(3,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
print("All threads finished.")
```

## 데몬 스레드

데몬 스레드는 메인 스레드가 종료될 때 자동으로 종료된다. `daemon=True` 옵션을 설정하여 데몬 스레드를 만들 수 있다. 데몬 스레드는 백그라운드에서 실행되는 작업에 적합하지만, 중요한 작업을 수행할 때는 일반 스레드를 사용해야 한다.

```python
def background_task():
    while True:
        print("Background task running...")
        time.sleep(2)

daemon = threading.Thread(target=background_task, daemon=True)
daemon.start()
time.sleep(5)
print("Main thread exiting; daemon thread will be killed.")
```

## 락과 동기화

스레드 간에 공유 자원을 사용할 때는 데이터 경쟁을 피하기 위해 락(`threading.Lock`)을 사용해야 한다. 예를 들어 여러 스레드가 같은 카운터를 갱신하는 경우 다음과 같이 락을 사용할 수 있다.

```python
counter = 0
lock = threading.Lock()

def increment(times: int) -> None:
    global counter
    for _ in range(times):
        with lock:
            temp = counter
            temp += 1
            counter = temp

threads = [threading.Thread(target=increment, args=(10000,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print("Counter:", counter)
```

`threading` 모듈은 `Semaphore`, `Event`, `Condition` 등의 동기화 도구와 `ThreadPoolExecutor`(concurrent.futures에서 제공)를 통한 스레드 풀도 함께 제공한다. 스레딩은 I/O‑바운드 프로그램의 응답성을 높이는 도구지만, GIL 때문에 CPU‑집약적 병렬화에는 한계가 있음을 기억하자【570737854010064†L77-L150】.