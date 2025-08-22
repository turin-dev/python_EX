---

# 함수 정의와 호출

## 함수란?

- 특정 작업을 묶어 재사용하기 위한 코드 블록입니다.
- `def` 키워드로 함수를 정의하며, 함수 이름과 괄호 안의 매개변수 목록이 뒤따릅니다【558541776123640†L533-L553】.
- 함수 몸체는 다음 줄부터 들여쓰기로 구분하고, 첫 줄에 문자열을 쓰면 문서 문자열(docstring)이 됩니다【558541776123640†L555-L560】.

## 매개변수와 반환값

- 함수는 0개 이상의 인자를 받을 수 있고, `return` 문을 사용하여 값을 반환할 수 있습니다【558541776123640†L624-L627】.
- `return`을 생략하거나 반환식이 없으면 `None`을 반환합니다.
- 위치 전용 매개변수(`/`)와 키워드 전용 매개변수(`*`)를 사용하여 인자의 형식을 명확히 지정할 수 있습니다【192188866110884†L193-L233】.
- 가변 위치 인자 `*args`와 가변 키워드 인자 `**kwargs`를 사용하면 개수와 이름이 다양한 인자를 받을 수 있습니다.

## 예제: 피보나치 수열 출력

```python
def fib(n):
    """n보다 작은 피보나치 수열을 출력"""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()

fib(2000)
```

위 코드는 주어진 정수 n보다 작은 피보나치 수열을 출력합니다.

## 예제: 리스트 반환

```python
def fib_list(n):
    """n보다 작은 피보나치 수열을 리스트로 반환"""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result

print(fib_list(100))
```

## 예제: 위치 전용 매개변수와 키워드 전용 매개변수

```python
def f(a, b, /, c, d, *, e, f):
    print(a, b, c, d, e, f)

f(10, 20, 30, d=40, e=50, f=60)
```

위 함수에서 `/` 앞의 a와 b는 위치 인자로만 전달할 수 있고, `*` 뒤의 e와 f는 키워드 인자로만 전달해야 합니다【192188866110884†L193-L233】.

## 요약

함수는 코드를 모듈화하고 재사용성을 높여 복잡한 프로그램을 더 구조적으로 작성할 수 있게 합니다. 적절한 매개변수 정의와 반환값을 사용하여 명확한 API를 디자인하는 것이 중요합니다.

## 고급 기능

### 기본 인자(default argument)와 주의사항

함수의 매개변수에 기본값을 지정하면 호출 시 해당 인자를 생략할 수 있습니다. 기본값은 함수 정의 시점에 한 번만 평가되어 저장됩니다【558541776123640†L644-L694】. 따라서 기본값으로 리스트나 딕셔너리 같은 가변 객체를 사용하면 모든 호출에서 하나의 객체를 공유하게 되어 예상치 못한 동작이 발생할 수 있습니다【558541776123640†L692-L724】.

```python
def append_once(value, seq=[]):
    # 주의: seq는 정의 시점에 한 번만 생성됨
    seq.append(value)
    return seq

print(append_once(1))  # [1]
print(append_once(2))  # [1, 2] - 누적됨!

# 안전한 방법
def append_safe(value, seq=None):
    if seq is None:
        seq = []
    seq.append(value)
    return seq
```

### 키워드 인자와 가변 인자

함수를 호출할 때 `kwarg=value` 형태로 키워드를 지정하면 인자의 순서를 변경할 수 있습니다. 모든 키워드 인자는 위치 인자 뒤에 배치되어야 하며, 각 인자는 한 번만 지정할 수 있습니다【558541776123640†L724-L769】. `“*args”`는 임의 개수의 위치 인자를 튜플로 받고, `**kwargs`는 임의 개수의 키워드 인자를 딕셔너리로 받습니다【558541776123640†L781-L819】.

```python
def cheeseshop(kind, *args, **kwargs):
    print(f"-- Do you have any {kind}?")
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(key, ':', value)

cheeseshop("Limburger", "It's very runny", shopkeeper="Michael Palin", client="John Cleese")
```

### 재귀 함수와 꼬리 재귀

함수가 자기 자신을 호출하면 재귀가 됩니다. 재귀는 문제를 더 작은 문제로 분할하여 해결할 때 유용합니다. 예를 들어 팩토리얼 계산:

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

print(factorial(5))  # 120
```

일부 언어에서는 꼬리 재귀 최적화가 지원되지만 파이썬 인터프리터는 이를 자동으로 수행하지 않으므로 재귀 깊이에 주의해야 합니다.

### 클로저와 `nonlocal`

중첩 함수는 바깥 함수의 변수를 참조할 수 있습니다. 내부 함수에서 변수를 수정하려면 `nonlocal` 선언을 사용해야 합니다. `nonlocal`은 가장 가까운 외부 스코프의 변수를 재바인딩하는 키워드입니다【558541776123640†L556-L570】.

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
```

### 문서 문자열과 타입 힌트

함수 첫 줄에 문자열을 작성하면 문서 문자열(docstring)이 되어 `help()` 함수나 문서 생성 도구에서 사용됩니다. 첫 줄은 간결한 요약이어야 하며 두 번째 줄은 비워 가독성을 높입니다【558541776123640†L1094-L1108】.

또한 파라미터와 반환값에 타입 힌트를 지정할 수 있으며 이는 런타임에 강제되지 않는 선택적 메타데이터입니다【558541776123640†L1140-L1159】.

```python
def greet(name: str, age: int = 0) -> str:
    """사용자의 이름과 나이를 입력받아 인사 문장을 반환합니다."""
    return f"안녕하세요, {name}({age})님!"

print(greet('투린', 14))
print(greet.__annotations__)
```