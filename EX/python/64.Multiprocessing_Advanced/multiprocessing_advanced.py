"""Advanced multiprocessing examples: shared memory and manager objects."""

from __future__ import annotations

import multiprocessing as mp
from multiprocessing import shared_memory


def increment_shared(name: str) -> None:
    shm = shared_memory.SharedMemory(name=name)
    buf = shm.buf
    # increment each element
    for i in range(len(buf)):
        buf[i] += 1
    shm.close()


def shared_memory_demo() -> None:
    size = 5
    shm = shared_memory.SharedMemory(create=True, size=size)
    shm.buf[:size] = b"abcde"
    print("Original buffer:", bytes(shm.buf[:size]))
    processes = [mp.Process(target=increment_shared, args=(shm.name,)) for _ in range(3)]
    for p in processes: p.start()
    for p in processes: p.join()
    print("After increments:", bytes(shm.buf[:size]))
    shm.close(); shm.unlink()


def manager_demo() -> None:
    with mp.Manager() as manager:
        shared_list = manager.list([0, 0, 0])

        def worker(lst):
            for i in range(len(lst)):
                lst[i] += 1

        processes = [mp.Process(target=worker, args=(shared_list,)) for _ in range(4)]
        for p in processes: p.start()
        for p in processes: p.join()
        print("Shared list after updates:", list(shared_list))


if __name__ == "__main__":
    shared_memory_demo()
    manager_demo()