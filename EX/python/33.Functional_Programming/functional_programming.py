"""예제 33: itertools와 functools를 활용한 함수형 프로그래밍.

이 스크립트는 itertools의 반복자와 functools의 고차 함수를 사용하여
데이터를 처리하는 다양한 패턴을 보여 준다.
"""

from itertools import count, cycle, repeat, accumulate, chain
from functools import lru_cache, partial, reduce
import operator


def demo_itertools() -> None:
    # count와 zip을 이용하여 인덱스 붙이기
    letters = ['x', 'y', 'z']
    for index, letter in zip(count(1), letters):
        print(index, letter)
    # accumulate로 누적 합계
    nums = [1, 2, 3, 4]
    print('Accumulated sums:', list(accumulate(nums)))
    # chain으로 여러 이터러블 연결
    combined = list(chain('abc', [1, 2, 3]))
    print('Chained:', combined)


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    """재귀 피보나치 – lru_cache로 메모이제이션."""
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


def demo_functors() -> None:
    # partial을 사용하여 특정 인자를 고정한 함수 생성
    power_of_two = partial(pow, 2)
    print('2^5 =', power_of_two(5))
    # reduce를 사용해 리스트 곱셈 수행
    nums = [2, 3, 4]
    product = reduce(operator.mul, nums, 1)
    print('Product:', product)


if __name__ == '__main__':
    demo_itertools()
    print('Fibonacci(10):', fib(10))
    demo_functors()