"""예제 25: 멀티프로세싱을 이용한 병렬 계산.

이 스크립트는 CPU‑집약적인 작업을 여러 프로세스로 분산시키고 결과를 수집하는
방법을 보여 준다. `multiprocessing.Pool`을 사용하여 제곱 계산을 병렬로 수행한다.
"""

from multiprocessing import Pool


def compute_square(n: int) -> int:
    """정수를 제곱하여 반환한다 (CPU‑집약적 작업 예시)."""
    # 무의미한 루프를 통해 시간을 소비하여 CPU 부하를 만들 수 있다
    total = 0
    for _ in range(1000000):
        total += 1
    return n * n


def main() -> None:
    numbers = list(range(10))
    with Pool() as pool:
        squares = pool.map(compute_square, numbers)
    print("Squares:", squares)


if __name__ == '__main__':
    main()