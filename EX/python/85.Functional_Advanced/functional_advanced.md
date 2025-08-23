# 제85장 – 함수형 프로그래밍 도구 심화

파이썬의 `itertools`와 `functools` 모듈은 함수형 프로그래밍을 위한 강력한 도구를 제공합니다. 이러한 도구는 조합 가능한 이터레이터, 고차 함수와 데코레이터를 통해 코드 재사용성과 명료성을 높여 줍니다. `itertools` 문서는 이러한 구성 요소를 “빠르고 메모리 효율적인 도구”로 설명합니다【912455807076022†L51-L99】. `functools` 모듈에는 제네릭 함수 디스패치, 데코레이터, 캐싱 유틸리티가 포함되어 있습니다【974880726755322†L56-L69】【974880726755322†L70-L87】【974880726755322†L98-L121】.

## `itertools`를 이용한 조합

앞서 소개한 `count`, `cycle`, `accumulate` 외에도 `itertools`에는 조합을 생성하는 여러 이터레이터가 있습니다:

* `itertools.product(*iterables, repeat=1)` – 카테시안 곱을 생성합니다.
* `itertools.permutations(iterable, r=None)` – 길이 `r`인 순열을 생성합니다.
* `itertools.combinations(iterable, r)` – 길이 `r`인 조합을 생성합니다.
* `itertools.combinations_with_replacement(iterable, r)` – 중복을 허용하는 조합을 생성합니다.

이러한 이터레이터는 결과를 지연(lazy) 생성하므로 큰 입력에 대해 메모리를 효율적으로 사용합니다.

## 단일 디스패치 제네릭 함수

`functools.singledispatch`는 함수를 단일 디스패치 제네릭 함수로 바꿉니다. 특정 타입에 대한 구현을 `@<함수>.register` 데코레이터로 등록합니다. 런타임에는 첫 번째 인자의 타입에 따라 적절한 구현이 선택됩니다【974880726755322†L56-L69】.

```python
from functools import singledispatch

@singledispatch
def serialize(obj) -> str:
    raise NotImplementedError("Unsupported type")

@serialize.register
def _(s: str) -> str:
    return s

@serialize.register
def _(n: int) -> str:
    return str(n)

print(serialize("hello"))  # 'hello'
print(serialize(42))       # '42'
```

## 데코레이터와 캐싱

`functools` 모듈은 `lru_cache(maxsize=None)`와 `cache()`와 같은 메모이제이션 데코레이터를 제공합니다. `total_ordering`은 `__lt__`와 `__eq__`를 기반으로 나머지 비교 메서드를 생성합니다【974880726755322†L98-L121】. `partial()`은 일부 인수를 고정한 새로운 호출 가능 객체를 생성하여 커링과 함수 합성을 가능하게 합니다【974880726755322†L70-L87】.

## 요약

`itertools`를 사용해 효율적인 이터레이션을 구현하고, `functools`를 사용해 제네릭 함수, 캐싱 및 데코레이터를 활용하세요. 이러한 모듈은 파이썬에서 함수형 프로그래밍 스타일을 구현하는 데 도움이 되며, 단순하면서도 메모리 효율적입니다【912455807076022†L51-L99】【974880726755322†L56-L69】【974880726755322†L70-L87】【974880726755322†L98-L121】.