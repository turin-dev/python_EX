"""예제 24: 스레드를 사용한 병렬 I/O 작업.

이 스크립트는 `threading` 모듈로 여러 스레드를 생성하여 공유 카운터를 증가시키고,
데몬 스레드의 동작을 보여 준다.
"""

import threading
import time


counter = 0
lock = threading.Lock()


def increment(times: int) -> None:
    """공유 카운터를 주어진 횟수만큼 증가시킨다."""
    global counter
    for _ in range(times):
        with lock:
            counter += 1


def background():
    """무한 루프를 도는 데몬 스레드 작업."""
    while True:
        print("Daemon thread running...")
        time.sleep(2)


def run_demo():
    threads = [threading.Thread(target=increment, args=(100000,)) for _ in range(4)]
    for t in threads:
        t.start()

    # 데몬 스레드 시작
    daemon = threading.Thread(target=background, daemon=True)
    daemon.start()

    for t in threads:
        t.join()
    print("Counter value:", counter)
    # 데몬 스레드가 백그라운드에서 실행되지만, 메인 스레드가 끝나면 종료된다.
    print("Main thread exiting; daemon will be killed.")


if __name__ == '__main__':
    run_demo()