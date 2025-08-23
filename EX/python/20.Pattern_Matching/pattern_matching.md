---

# 패턴 매칭 (match / case)

## match 문이란?

- Python 3.10부터 도입된 구조적 패턴 매칭은 값의 구조를 기반으로 여러 경우를 깔끔하게 처리할 수 있도록 합니다.
- `match` 키워드와 여러 `case` 블록으로 구성되며, 첫 번째로 일치하는 패턴이 실행됩니다【558541776123640†L345-L365】.

## 기본 사용 예제

```python
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"
```

## 패턴 묶기와 변수 캡처

- 여러 리터럴을 `|` 기호로 묶어 하나의 `case`에서 처리할 수 있습니다【558541776123640†L370-L375】.
- 패턴에서 튜플이나 리스트 구조를 사용하면 값을 분해하고 변수에 할당할 수 있습니다【558541776123640†L381-L390】.

```python
point = (0, 5)
match point:
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        print("기타")
```

## 클래스와 매핑 패턴

- 클래스 이름과 필드명을 사용하여 객체의 속성을 기반으로 매칭할 수 있습니다【558541776123640†L400-L423】.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def where_is(p):
    match p:
        case Point(x=0, y=0):
            return "원점"
        case Point(x=0, y=y):
            return f"Y={y}"
        case Point(x=x, y=0):
            return f"X={x}"
        case Point():
            return "기타"
        case _:
            return "점이 아님"
```

## 가드와 기타 패턴

- 패턴 뒤에 `if` 조건을 추가하여 더 복잡한 조건을 표현할 수 있습니다【558541776123640†L467-L492】.
- 리스트, 딕셔너리 등 여러 구조에 대한 패턴 매칭과 변수 바인딩을 지원합니다.

## 요약

패턴 매칭은 `if`/`elif` 체인을 대체하여 코드의 가독성을 높여줍니다. 다양한 구조와 조건을 선언적으로 표현할 수 있으며, 특히 데이터 구조를 해체하여 변수에 바인딩하는 데 유용합니다.

## 추가 설명

### 별표 패턴과 시퀀스 분해

`case [x, *rest]`와 같이 별표(`*`)를 사용하면 시퀀스의 나머지 요소를 리스트로 포착할 수 있습니다. 이는 가변 길이 시퀀스를 처리할 때 유용합니다.

```python
def describe(seq):
    match seq:
        case []:
            return '빈 시퀀스'
        case [x]:
            return f'한 요소: {x}'
        case [first, *rest]:
            return f'첫 요소: {first}, 나머지: {rest}'

print(describe([1, 2, 3]))  # 첫 요소: 1, 나머지: [2, 3]
```

### 매핑 패턴과 가드

딕셔너리와 비슷한 매핑 객체에 대해 키와 값을 매칭할 수 있습니다. 패턴 뒤에 `if` 가드를 추가하여 추가 조건을 지정할 수 있습니다.

```python
def price(info):
    match info:
        case {'item': item, 'price': p} if p > 100:
            return f'{item} is expensive'
        case {'item': item, 'price': p}:
            return f'{item} costs {p}'
        case _:
            return '알 수 없는 정보'

print(price({'item': 'pen', 'price': 50}))
```

### 클래스 패턴과 `__match_args__`

클래스 패턴은 생성자 매개변수나 `__match_args__` 속성에 정의된 필드명 순서에 따라 값을 추출합니다. 사용자 정의 클래스에서 패턴 매칭을 지원하려면 `__match_args__` 튜플을 정의하거나 PEP 636에 따라 `dataclasses.dataclass`를 사용합니다.

```python
class Point3D:
    __match_args__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

p = Point3D(1, 2, 3)
match p:
    case Point3D(x, y, z):
        print(x, y, z)
```

### 제한 사항

패턴 매칭은 값의 구조를 비교하는 기능으로, 정규 표현식과 다르게 문자열 패턴을 인식하지 않습니다. 또한 부동소수점과 정수 간의 암묵적인 일치는 발생하지 않으므로 주의해야 합니다. 패턴은 첫 번째 일치하는 분기를 실행하고, 나머지는 검사하지 않습니다.