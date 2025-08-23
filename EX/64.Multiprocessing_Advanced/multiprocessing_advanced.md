# 제64장 – 고급 멀티프로세싱: 공유 메모리와 매니저

`multiprocessing` 모듈은 전역 인터프리터 잠금(GIL)을 우회하기 위해 별도의 파이썬 프로세스를 생성하므로 여러 CPU 코어를 최대한 활용할 수 있습니다. 그러나 프로세스는 메모리를 공유하지 않기 때문에 데이터를 교환하려면 명시적인 메커니즘이 필요합니다. 문서에서는 `ProcessPoolExecutor`에 전달되는 함수와 객체는 피클링할 수 있어야 하고, 인터랙티브 셸이 아닌 임포트 가능한 모듈에 정의되어야 한다고 강조합니다【831315557977939†L274-L289】.

## 공유 메모리

Python 3.8에서 도입된 `multiprocessing.shared_memory`는 여러 프로세스가 접근할 수 있는 저수준 공유 메모리 블록을 제공합니다. `SharedMemory` 객체를 생성하여 메모리 블록을 할당한 뒤 `memoryview`로 감싸서 다른 프로세스에서 같은 블록을 사용할 수 있습니다. 이 방법은 큰 배열을 피클링하는 오버헤드를 피할 수 있습니다. 상위 수준의 공유 객체로는 `multiprocessing.Array`와 `multiprocessing.Value`가 있으며, 이는 ctypes 기반의 공유 메모리를 제공합니다.

```python
from multiprocessing import Process, shared_memory

def child(name):
    # 기존 공유 메모리에 연결
    shm = shared_memory.SharedMemory(name=name)
    buf = shm.buf
    # 첫 바이트를 증가시킴
    buf[0] += 1
    shm.close()

shm = shared_memory.SharedMemory(create=True, size=10)
shm.buf[0] = 42
print("Parent value:", shm.buf[0])

p = Process(target=child, args=(shm.name,))
p.start(); p.join()
print("After child:", shm.buf[0])
shm.close(); shm.unlink()
```

## 매니저와 프록시

`multiprocessing.Manager`는 별도의 서버 프로세스를 생성하여 Python 객체를 보관하고 자식 프로세스에 프록시합니다. 매니저는 리스트, 딕셔너리, 큐, 네임스페이스 등 복잡한 구조를 공유할 수 있는 편리한 인터페이스를 제공합니다. 저수준 공유 메모리를 직접 다루지 않고도 복잡한 객체를 여러 프로세스 간에 공유해야 할 때 매니저를 사용하세요.

```python
from multiprocessing import Manager, Process

with Manager() as manager:
    shared_dict = manager.dict()
    shared_dict["count"] = 0

    def worker(d):
        for _ in range(10000):
            d["count"] += 1

    processes = [Process(target=worker, args=(shared_dict,)) for _ in range(4)]
    for p in processes: p.start()
    for p in processes: p.join()
    print("Final count:", shared_dict["count"])  # 40000
```

이와 같이 고급 멀티프로세싱에서는 공유 메모리와 매니저를 통해 프로세스 간 데이터를 효율적으로 교환할 수 있습니다.