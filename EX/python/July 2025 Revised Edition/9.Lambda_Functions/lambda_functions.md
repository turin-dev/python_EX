---

# 람다와 고차 함수

## 람다(lambda) 표현식

- 간단한 익명 함수를 정의할 때 사용합니다.
- 형식은 `lambda 매개변수들: 식`으로, 표현식만을 포함해야 하며 한 줄로 작성합니다.

```python
square = lambda x: x * x
print(square(5))  # 25
```

## 고차 함수

함수를 인자로 받거나 함수를 반환하는 함수를 고차 함수(high‑order function)라고 합니다. 파이썬의 내장 함수 중 `map()`, `filter()`, `reduce()`가 대표적인 예입니다.

- `map(function, iterable)`: 각 요소에 함수를 적용합니다.
- `filter(function, iterable)`: 조건식이 참인 요소만 남깁니다.
- `reduce(function, sequence[, initial])`: 누적 함수를 적용하여 하나의 값으로 축약합니다. 사용하려면 `functools.reduce`를 가져와야 합니다.

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
product = reduce(lambda x, y: x * y, numbers)
print(squares)  # [1, 4, 9, 16, 25]
print(evens)   # [2, 4]
print(product) # 120
```

## 람다와 컴프리헨션 비교

- 람다를 `map`/`filter`와 함께 사용하는 것보다 리스트 컴프리헨션이 가독성과 성능 면에서 더 좋은 경우가 많습니다.
- 예: 각 단어의 길이 구하기

```python
words = ['Python', 'Java', 'C']
lengths1 = list(map(len, words))
lengths2 = [len(w) for w in words]  # 더 간결
print(lengths1)
print(lengths2)
```

## 요약

람다 표현식은 작고 익명의 함수를 빠르게 정의하는 데 유용합니다. `map()`, `filter()`, `reduce()` 등의 고차 함수와 함께 사용할 수 있지만, 많은 경우 리스트 컴프리헨션이 더 명확하고 성능이 좋습니다.

## 추가 설명과 활용 예제

### 정렬과 키 함수

람다 표현식은 정렬의 키 함수로 자주 사용됩니다. `sorted()`나 `list.sort()`에 `key` 매개변수를 전달하여 각 요소에 대한 비교 기준을 정의할 수 있습니다.

```python
words = ['apple', 'Banana', 'cherry']
print(sorted(words, key=lambda w: w.lower()))  # 대소문자 구분 없이 정렬
```

위 예제처럼 간단한 함수를 전달할 때 람다가 편리하지만, 복잡한 키 함수를 사용할 경우 `operator` 모듈의 `itemgetter`나 별도의 이름있는 함수를 사용하는 것이 더 읽기 쉽습니다.

### any, all, sum 과 함께 사용

람다 표현식과 고차 함수 외에도 `any()`와 `all()`과 같은 내장 함수는 시퀀스 전체에 대한 조건을 판단할 때 유용합니다. 아래 예제는 모든 숫자가 짝수인지 확인합니다.

```python
numbers = [2, 4, 6]
is_all_even = all(map(lambda x: x % 2 == 0, numbers))
print(is_all_even)  # True
```

### functools.partial

`functools.partial`을 사용하면 일부 인자를 고정한 새로운 함수를 생성할 수 있어 람다를 대신할 수 있습니다. 이는 재사용 가능한 함수를 만들 때 유용합니다.

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5), cube(2))  # 25 8
```

### 주의사항

람다 표현식은 한 줄짜리 익명 함수를 정의할 수 있지만, 너무 복잡한 연산을 담기 시작하면 가독성이 떨어집니다. 이 경우에는 `def`로 함수를 정의하여 이름을 부여하고 주석을 추가하는 것이 좋습니다.