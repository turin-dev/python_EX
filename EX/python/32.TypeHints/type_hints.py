"""예제 32: 타입 힌트를 활용한 함수와 데이터 구조.

이 스크립트는 기본적인 타입 힌트와 `typing` 모듈의 고급 타입
(`TypedDict`, `Protocol`, `Literal`) 사용 예를 보여 준다.
"""

from typing import TypedDict, Protocol, Literal, Optional, Union


def greet(name: str) -> str:
    return f"Hello, {name}!"


def maybe_divide(x: float, y: float) -> Optional[float]:
    if y == 0:
        return None
    return x / y


class User(TypedDict):
    username: str
    email: str
    age: int


def print_user(user: User) -> None:
    print(f"{user['username']} <{user['email']}> ({user['age']})")


class SupportsLen(Protocol):
    def __len__(self) -> int: ...


def show_length(item: SupportsLen) -> None:
    print(f"Length is {len(item)}")


Mode = Literal['r', 'w', 'a']


def open_file(path: str, mode: Mode) -> None:
    print(f"Would open {path} with mode {mode}")


if __name__ == '__main__':
    print(greet('Type Hints'))
    print(maybe_divide(10, 2), maybe_divide(10, 0))
    user: User = {'username': 'alice', 'email': 'alice@example.com', 'age': 30}
    print_user(user)
    show_length([1, 2, 3, 4])
    open_file('example.txt', 'r')