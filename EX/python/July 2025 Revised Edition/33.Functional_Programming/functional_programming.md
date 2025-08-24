# 33. 함수형 프로그래밍 도구

파이썬은 리스트 컴프리헨션과 제너레이터 외에도 고차 함수와 이터레이터를 지원하는 다양한 도구를 제공한다. 이 장에서는 `itertools`와 `functools` 모듈의 주요 기능을 살펴본다.

## `itertools` — 효율적인 반복자

`itertools` 모듈은 *메모리 효율적인 반복자 빌딩 블록*을 제공하며 이를 통해 반복자의 대수(알제브라)를 구성할 수 있다고 설명한다【912455807076022†L51-L99】. 주요 함수는 다음과 같다.

- `count(start=0, step=1)`: 무한한 정수 시퀀스를 생성한다.
- `cycle(iterable)`: 주어진 시퀀스를 반복적으로 순환한다.
- `repeat(elem, n=None)`: 주어진 요소를 반복적으로 반환한다.
- `accumulate(iterable, func=operator.add)`: 누적 합계 혹은 누적 연산을 수행한다.
- `chain(*iterables)`: 여러 이터러블을 순차적으로 연결한다.
- `combinations(iterable, r)`, `permutations(iterable, r)`: 조합과 순열 생성.

예를 들어, 무한 카운터와 `map`을 조합해 인덱스가 붙은 리스트를 생성할 수 있다【912455807076022†L51-L99】:

```python
from itertools import count, islice

letters = ['a', 'b', 'c']
indexed = list(zip(count(1), letters))
print(indexed)  # [(1, 'a'), (2, 'b'), (3, 'c')]
```

`itertools`는 불변의 순열 생성이나 무한 반복 등에서 메모리 사용을 최소화하므로, 대용량 데이터나 스트림 처리에 유용하다.

## `functools` — 고차 함수와 데코레이터

`functools` 모듈은 다른 함수를 인자로 받거나 함수를 반환하는 고차 함수들을 제공한다【974880726755322†L56-L58】. 대표적인 기능은 다음과 같다.

- `functools.cache`: 인자로 주어진 함수에 대한 **제한 없는 메모이제이션**을 제공한다. 이는 `lru_cache(maxsize=None)`와 동일하며, 반복 호출 시 저장된 결과를 반환해 성능을 높인다【974880726755322†L56-L69】.
- `functools.lru_cache(maxsize=128)`: 최근 사용 결과를 캐시하는 메모이제이션. `maxsize`를 지정하여 오래된 결과를 제거한다.
- `functools.partial(func, *args, **kwargs)`: 일부 인자를 고정한 새로운 함수를 생성한다. 반복적으로 비슷한 인자를 넘길 때 편리하다.
- `functools.reduce(function, iterable, initial=None)`: 반복 가능한 자료에 함수를 누적 적용해 단일 값으로 축소한다.
- `functools.cached_property`: 클래스 메서드를 **한 번만 계산하여 캐시**하고 이후에는 속성처럼 접근하게 한다【974880726755322†L98-L121】.

```python
from functools import lru_cache, reduce

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    return n if n < 2 else fib(n-1) + fib(n-2)

print(fib(30))  # 캐시 덕분에 빠르게 계산

# reduce를 사용하여 곱셈 수행
nums = [1, 2, 3, 4]
product = reduce(lambda x, y: x * y, nums, 1)
print(product)  # 24
```

`itertools`와 `functools`는 함수형 프로그래밍 패러다임을 지원하며, 반복 작업의 복잡도를 줄이고 코드의 재사용성을 높이는 데 도움이 된다.