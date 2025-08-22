---

# 이터레이터와 제너레이터

## 이터레이터(iterator)

- 순차적으로 값을 반환하는 객체로, `__iter__()`와 `__next__()` 메서드를 구현합니다.
- `for` 문은 내부적으로 이터레이터를 사용하여 반복을 수행합니다.

```python
it = iter([1, 2, 3])
print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3
```

## 제너레이터(generator)

- `yield` 키워드를 사용하여 값을 하나씩 생성하는 함수입니다.
- 제너레이터는 필요할 때만 값을 생성하므로 메모리 사용이 효율적입니다.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for i in countdown(3):
    print(i)
```

## 제너레이터 표현식(generator expression)

- 리스트 컴프리헨션과 비슷하지만 괄호 `()`를 사용하여 한 번에 하나의 값을 생성합니다.

```python
squares = (x**2 for x in range(5))
for s in squares:
    print(s)
```

## 요약

이터레이터는 반복 가능한 객체를 하나씩 반환하는 메커니즘이고, 제너레이터는 `yield`를 통해 이터레이터를 쉽게 정의하는 방법입니다. 제너레이터 표현식을 사용하면 메모리 효율적인 반복을 간결하게 표현할 수 있습니다.

## 추가 설명

### 사용자 정의 이터레이터

모든 이터러블 객체는 `__iter__()` 메서드를 구현하여 이터레이터를 반환하고, 이터레이터는 `__next__()` 메서드를 구현하여 다음 값을 생성해야 합니다. `StopIteration` 예외를 발생시키면 반복이 종료됩니다.

```python
class CountDown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

for i in CountDown(3):
    print(i)
```

### 제너레이터 고급 기능

제너레이터 함수는 `yield` 표현식으로 양방향 통신을 할 수 있습니다. `generator.send(value)`는 제너레이터의 `yield` 표현식에 값을 전달하고 실행을 재개합니다. `yield from` 구문은 다른 제너레이터나 이터러블을 위임하여 값들을 차례로 산출합니다.

```python
def echo():
    received = None
    while True:
        received = yield received

gen = echo()
next(gen)  # 제너레이터 초기화
print(gen.send('hello'))  # hello
print(gen.send('world'))  # world

def nested():
    yield from range(3)
    yield from ['a', 'b']

print(list(nested()))  # [0, 1, 2, 'a', 'b']
```

### itertools 모듈

`itertools`는 이터레이터에 대한 고성능 함수들을 제공하는 표준 라이브러리입니다. `chain()`은 여러 이터러블을 이어 붙이고, `islice()`는 특정 구간을 잘라냅니다. `cycle()`은 시퀀스를 무한 반복하며, `product()`는 데카르트 곱을 생성합니다.

```python
from itertools import chain, islice, cycle, product

print(list(chain('ab', 'cd')))        # ['a', 'b', 'c', 'd']
print(list(islice(range(10), 3, 6)))  # [3, 4, 5]

for i, letter in zip(range(3), cycle('xy')):
    print(i, letter)  # (0, 'x'), (1, 'y'), (2, 'x')

print(list(product([1, 2], ['a', 'b'])))  # [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
```