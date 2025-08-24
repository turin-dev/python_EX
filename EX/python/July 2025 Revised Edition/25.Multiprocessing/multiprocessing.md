# 25. 멀티프로세싱: CPU‑바운드 병렬 처리

`multiprocessing` 모듈은 여러 프로세스를 생성하여 파이썬 프로그램을 병렬로 실행할 수 있게 한다. 이는 전역 인터프리터 잠금(GIL)을 우회하여 CPU‑집약적인 작업에서 여러 CPU 코어를 활용할 수 있게 한다. 문서에서는 *이 모듈이 스폰된 프로세스를 통해 GIL을 회피하고, `threading`과 유사한 API를 제공한다고 설명한다*【133981838125243†L91-L103】.

## 프로세스 기반 병렬화

기본적으로 `multiprocessing.Process`를 사용해 별도의 프로세스를 생성할 수 있다. 프로세스는 서로 메모리를 공유하지 않으므로, 데이트를 주고받으려면 큐나 파이프를 사용한다.

```python
from multiprocessing import Process

def cpu_bound_task(n: int) -> None:
    # n까지의 피보나치 합을 구하는 가짜 CPU 집약적 작업
    total = 0
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
        total += a
    print(f"Sum up to {n}: {total}")

if __name__ == '__main__':  # 윈도우에서 프로세스 생성 시 필요
    processes = [Process(target=cpu_bound_task, args=(50000,)) for _ in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print("All processes finished.")
```

## 프로세스 풀

반복 작업을 병렬로 수행해야 할 때는 `multiprocessing.Pool`을 사용하는 것이 편리하다. 풀은 지정된 개수의 워커 프로세스를 관리하고, 태스크를 분배한다.

```python
from multiprocessing import Pool

def square(x: int) -> int:
    return x * x

if __name__ == '__main__':
    with Pool() as pool:
        results = pool.map(square, range(10))
    print(results)  # [0, 1, 4, 9, ...]
```

## Queue와 파이프

프로세스 간 통신을 위해 `multiprocessing.Queue`나 `Pipe`를 사용할 수 있다. 큐는 스레드 안전하며 여러 프로세스 간에 데이터를 쉽게 전달할 수 있다.

멀티프로세싱은 병렬 계산 성능을 향상시키지만, 프로세스 간 메모리가 분리되어 있으므로 데이터 전달의 비용이 발생한다. 따라서 작업의 특성에 따라 스레딩, 비동기, 멀티프로세싱 중 적절한 도구를 선택해야 한다【133981838125243†L91-L103】.