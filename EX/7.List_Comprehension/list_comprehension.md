---

# 리스트와 컴프리헨션

## 리스트(list)

- 순서가 있는 가변 자료형으로 대괄호 `[]` 안에 여러 값을 저장합니다.
- 다양한 자료형을 포함할 수 있으며 인덱싱과 슬라이싱으로 요소에 접근합니다.
- 주요 메서드: `append()`, `extend()`, `insert()`, `remove()`, `pop()`, `sort()`, `reverse()` 등.

```python
fruits = ['apple', 'banana', 'cherry']
fruits.append('orange')
fruits.remove('banana')
print(fruits)  # ['apple', 'cherry', 'orange']
```

## 리스트 컴프리헨션

- 기존 리스트나 반복 가능한 객체를 기반으로 새로운 리스트를 간결하게 생성하는 구문입니다.
- 형식: `[식 for 항목 in 반복가능객체 if 조건]` — 조건은 생략할 수 있습니다.

```python
# 0부터 9까지 정수의 제곱
squares = [x**2 for x in range(10)]

# 짝수만 선택하여 제곱
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

- 중괄호 `{}` 를 사용하면 집합(set) 컴프리헨션, `{key: value for ...}` 형태로 딕셔너리 컴프리헨션을 만들 수 있습니다.
- 소괄호 `() `를 사용하면 제너레이터 표현식을 생성하여 필요한 순간에만 값을 계산합니다.

## 할당식(Walrus Operator)

- Python 3.8에서 도입된 할당식 `:=`는 표현식 내에서 값을 대입하고 동시에 사용할 수 있도록 합니다【192188866110884†L142-L171】.
- 컴프리헨션이나 조건식 안에서 중복된 계산을 방지하고 코드를 간결하게 만드는 데 유용합니다.

```python
allowed_names = {'python', 'java', 'rust'}
names = ['Python', 'JAVA', 'go', 'rust']
cleaned = [clean.title() for name in names if (clean := name.lower()) in allowed_names]
print(cleaned)  # ['Python', 'Java', 'Rust']
```

## 요약

리스트는 순서가 있는 가변 컨테이너로 다양한 메서드를 제공합니다. 리스트 컴프리헨션은 반복문과 조건식을 한 줄로 표현하여 새로운 리스트를 만들 수 있으며, 할당식(`:=`)을 이용하면 컴프리헨션 내에서 변수를 효율적으로 사용할 수 있습니다.

## 추가 설명과 고급 예제

### 리스트 메서드 상세

리스트는 많은 내장 메서드를 제공합니다. `append()`, `extend()`, `insert()`, `remove()`, `pop()`, `clear()`, `index()`, `count()`, `sort()`, `reverse()`, `copy()` 등이 대표적입니다【837034082833640†L69-L126】. 대부분의 메서드는 리스트 자체를 수정하고 `None`을 반환하므로 체인 호출이 불가능하다는 점을 유의하세요. 예를 들어 `numbers.append(4).sort()`는 오류를 발생시키며, 다음과 같이 두 단계로 나누어야 합니다.

```python
numbers = [3, 1, 4, 1, 5]
numbers.append(9)   # 리스트를 수정, 반환값은 None
numbers.sort()      # 정렬
print(numbers)      # [1, 1, 3, 4, 5, 9]
```

또한 `list.copy()`는 표면적으로는 얕은 복사를 제공하므로 중첩 리스트를 복사할 때는 `copy.deepcopy`를 사용해야 합니다.

### 중첩 컴프리헨션과 여러 for/if

리스트 컴프리헨션은 여러 개의 `for` 또는 `if` 절을 사용하여 중첩 반복과 조건을 표현할 수 있습니다【837034082833640†L212-L249】. 두 리스트의 모든 조합을 생성하는 예제는 다음과 같습니다.

```python
colors = ['red', 'green']
objects = ['apple', 'leaf']
pairs = [(c, o) for c in colors for o in objects]
print(pairs)  # [('red', 'apple'), ('red', 'leaf'), ('green', 'apple'), ('green', 'leaf')]
```

조건부 절을 여러 개 포함할 수도 있습니다. 아래 예제는 두 리스트에서 서로 같지 않은 조합만 추출합니다【837034082833640†L252-L268】.

```python
A = [1, 2, 3]
B = [3, 1, 4]
pairs = [(x, y) for x in A for y in B if x != y]
print(pairs)  # (1, 3), (1, 4), (2, 3), ...
```

### 행렬 전치와 `zip()`

다차원 리스트의 행과 열을 바꾸는 “전치(transpose)” 연산은 중첩 컴프리헨션으로 구현할 수 있습니다【837034082833640†L330-L347】.

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print(transposed)  # [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

하지만 이와 같은 복잡한 컴프리헨션은 읽기 어렵기 때문에 표준 함수 `zip()`을 사용하는 것이 더 명확하고 성능도 좋습니다【837034082833640†L364-L370】.

```python
# * 연산자로 리스트를 언패킹하여 zip에 전달
transposed2 = list(zip(*matrix))
```

### 딕셔너리·집합 컴프리헨션과 제너레이터 표현식

딕셔너리와 집합도 컴프리헨션을 통해 생성할 수 있습니다. 딕셔너리 컴프리헨션은 키와 값을 동시에 계산하며, 집합 컴프리헨션은 중복이 자동으로 제거됩니다. 제너레이터 표현식은 소괄호 `()`를 사용하며 필요한 순간에만 값을 생성해 메모리 사용량을 줄입니다.

```python
# 단어 길이 카운트 딕셔너리
words = ['python', 'java', 'c']
length_map = {w: len(w) for w in words}

# 모음 집합
vowels = {ch for ch in 'Hello World' if ch.lower() in 'aeiou'}

# 제너레이터 표현식으로 큰 수열을 지연 생성
squares_gen = (x**2 for x in range(1000000))
```

컴프리헨션이 너무 복잡해지면 일반 `for` 루프나 `zip()` 같은 내장 함수를 사용하는 편이 가독성이 좋습니다.