"""예제 22: 컨텍스트 매니저 사용법.

이 스크립트는 사용자 정의 컨텍스트 매니저 클래스와 `contextlib.contextmanager`
데코레이터를 이용한 제너레이터 기반 컨텍스트 매니저의 사용 예를 보여 준다.
"""

from contextlib import contextmanager
from typing import Generator, Iterable


class ManagedFile:
    """파일을 안전하게 열고 닫는 컨텍스트 매니저."""

    def __init__(self, filename: str, mode: str = 'w', encoding: str = 'utf-8'):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding=self.encoding)
        return self.file

    def __exit__(self, exc_type, exc, tb):
        if self.file:
            self.file.close()
        # 예외를 억제하지 않고 다시 전파한다.
        return False


@contextmanager
def open_uppercase(path: str) -> Generator[Iterable[str], None, None]:
    """파일을 열고 모든 줄을 대문자로 변환하는 제너레이터 기반 컨텍스트 매니저."""
    f = open(path, 'r', encoding='utf-8')
    try:
        yield (line.upper() for line in f)
    finally:
        f.close()


def demo():
    """컨텍스트 매니저의 사용 예를 보여 준다."""
    # 사용자 정의 클래스 사용
    with ManagedFile('managed.txt') as f:
        f.write('This file is managed by a context manager.')

    # 제너레이터 기반 매니저 사용
    # 읽을 파일을 미리 준비한다.
    with open('sample.txt', 'w', encoding='utf-8') as sample:
        sample.write('hello\nworld\n')
    
    with open_uppercase('sample.txt') as lines:
        for line in lines:
            print(line.strip())


if __name__ == '__main__':
    demo()