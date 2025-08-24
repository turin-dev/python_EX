---

# 딕셔너리와 집합

## 딕셔너리(dict)

- 키(key)와 값(value) 쌍을 저장하는 가변 자료형입니다.
- 중괄호 `{}` 또는 `dict()` 함수로 생성하며, 키는 해시 가능한 불변 객체여야 합니다.

```python
person = {"name": "투린", "age": 14}
print(person["name"])
person["age"] = 15
person["city"] = "포항"
for key, value in person.items():
    print(key, value)
```

- 메서드: `keys()`, `values()`, `items()`, `get(key, default)`, `update(other)`, `pop(key)` 등이 있습니다.

## 딕셔너리 컴프리헨션

- 리스트 컴프리헨션과 유사하게 `{키: 값 for 요소 in 반복가능객체}` 형태로 새로운 딕셔너리를 생성할 수 있습니다.

```python
squares = {x: x**2 for x in range(5)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

## 집합(set)

- 중복 없는 요소의 모음으로 순서가 없습니다.
- 중괄호 `{}` 또는 `set()` 함수로 생성합니다. 빈 집합을 생성할 때는 `{}`가 아니라 `set()`을 사용해야 합니다.

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a | b)  # 합집합: {1, 2, 3, 4}
print(a & b)  # 교집합: {2, 3}
print(a - b)  # 차집합: {1}
print(a ^ b)  # 대칭차집합: {1, 4}
```

- 집합은 요소의 존재 여부 검사나 중복 제거에 매우 효율적입니다.

## 요약

딕셔너리는 키‑값 쌍을 저장하는 유연한 자료형으로, 항목을 빠르게 조회하고 수정할 수 있습니다. 집합은 중복 없는 요소 모음을 표현하며, 합집합·교집합 등의 연산으로 수학적 집합 연산을 쉽게 수행할 수 있습니다.

## 추가 설명

### 딕셔너리 메서드와 순회

딕셔너리는 `get(key, default)`를 사용하여 키가 없을 때 기본값을 반환할 수 있습니다. `setdefault(key, default)`는 키가 없으면 기본값을 삽입하고 그 값을 반환합니다. `pop(key[, default])`는 키를 삭제하고 값을 반환하며, `del` 키워드를 사용하여 항목을 제거할 수도 있습니다. 파이썬 3.7부터 딕셔너리는 삽입 순서를 보존하므로, `keys()`, `values()`, `items()`로 얻는 뷰는 동적으로 연결되어 원본이 변경되면 함께 변경됩니다【837034082833640†L532-L576】.

```python
person = {'name': '투린', 'age': 14}
print(person.get('city', 'unknown'))  # 키가 없으면 기본값 반환
person.setdefault('city', '포항')
print(person['city'])

for key in person:  # 키만 순회
    print(key)
for key, value in person.items():  # 키와 값을 함께 순회
    print(key, value)
```

### 집합과 frozenset

집합은 해시 가능한 객체만 저장할 수 있으며, 중복을 제거하거나 멤버십 테스트에 적합합니다. `a <= b`는 부분집합 여부를, `a >= b`는 상위집합 여부를 판정합니다. `frozenset`은 불변 집합으로, 집합을 딕셔너리의 키로 사용하거나 집합 자체를 집합의 요소로 사용할 때 필요합니다【837034082833640†L480-L516】.

```python
a = {1, 2, 3}
b = {1, 2, 3, 4}
print(a <= b)  # True (부분집합)
print(b >= a)  # True (상위집합)

fs = frozenset([1, 2])
print(fs)

# 집합 컴프리헨션
squares_set = {x*x for x in range(5)}
print(squares_set)
```

## 참고

딕셔너리의 키는 불변 타입이어야 하며, 리스트처럼 가변 객체를 사용할 수 없습니다. 집합은 요소의 순서를 보장하지 않으므로 정렬된 결과가 필요할 때는 `sorted()` 함수를 사용하세요.