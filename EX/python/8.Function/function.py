# 함수 예제

def fib(n):
    """n보다 작은 피보나치 수열을 출력"""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()


def fib_list(n):
    """n보다 작은 피보나치 수열을 리스트로 반환"""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result


def f(a, b, /, c, d, *, e, f):
    """위치 전용과 키워드 전용 매개변수를 사용하는 예제 함수"""
    print(a, b, c, d, e, f)


if __name__ == "__main__":
    # 함수 호출 예제
    fib(50)
    print(fib_list(50))
    # 위치 전용과 키워드 전용 매개변수 사용 예제
    f(10, 20, 30, d=40, e=50, f=60)

    # 기본 인자와 안전한 인자 사용 예제
    def append_once(value, seq=[]):
        seq.append(value)
        return seq

    def append_safe(value, seq=None):
        if seq is None:
            seq = []
        seq.append(value)
        return seq

    print('append_once calls:', append_once(1), append_once(2))
    print('append_safe calls:', append_safe(1), append_safe(2))

    # 재귀 함수 예제: 팩토리얼
    def factorial(n):
        if n == 0:
            return 1
        return n * factorial(n-1)

    print('factorial(5):', factorial(5))

    # 클로저와 nonlocal 예제
    def make_counter():
        count = 0
        def increment():
            nonlocal count
            count += 1
            return count
        return increment

    counter = make_counter()
    print('counter values:', counter(), counter())

    # 문서 문자열과 타입 힌트 사용 예제
    def greet(name: str, age: int = 0) -> str:
        """사용자의 이름과 나이를 입력받아 인사 문장을 반환합니다."""
        return f"안녕하세요, {name}({age})님!"

    print(greet('투린', 14))
    print('annotations:', greet.__annotations__)