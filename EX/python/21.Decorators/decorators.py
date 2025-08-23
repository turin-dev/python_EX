"""예제 21: 데코레이터 활용 예.

이 스크립트는 파이썬의 데코레이터가 어떻게 동작하는지 보여준다. 로그를 출력하는
데코레이터와 반복 호출 데코레이터, 내장된 메모이제이션 데코레이터를 포함한다.
"""

from functools import wraps, cache
from time import sleep


def log_call(func):
    """함수 호출과 반환값을 출력하는 데코레이터."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result

    return wrapper


def repeat(n):
    """지정한 횟수만큼 함수를 호출하는 데코레이터."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(n):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@log_call
def add(a: int, b: int) -> int:
    """두 수를 더한 값을 반환한다."""
    return a + b


@repeat(3)
def greet(name: str) -> None:
    """인사를 여러 번 출력한다."""
    print(f"Hello, {name}!")


@cache
def fibonacci(n: int) -> int:
    """재귀적으로 피보나치 수열을 계산한다. 결과는 cache 데코레이터로
    메모이제이션된다"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    # 로그 데코레이터 사용
    add(2, 5)

    # 반복 데코레이터 사용
    greet("World")

    # 메모이제이션 데코레이터 사용
    print("Fibonacci(10)", fibonacci(10))