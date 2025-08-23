# 제89장 – 구조적 패턴 매칭 심화

파이썬 3.10에서는 `match`/`case` 문을 이용한 구조적 패턴 매칭이 도입되어 보다 표현력 있는 분기를 작성할 수 있게 되었습니다. 패턴은 리터럴 값, 변수 캡처, 시퀀스·객체 해체, 가드 등을 포함할 수 있습니다. PEP 636 튜토리얼은 시퀀스 패턴이 고정 길이 리스트와 일치하고, 변수 바인딩과 나머지(`*rest`) 패턴을 지원하는 방식을 설명합니다【372741329340159†L101-L116】.

## 시퀀스와 매핑 패턴

시퀀스 패턴에서는 개별 요소를 지정하고 스타 패턴으로 나머지를 캡처할 수 있습니다. 매핑 패턴은 딕셔너리에서 키로 매칭합니다.

```python
def describe(seq):
    match seq:
        case []:
            return "empty"
        case [x]:
            return f"single element {x}"
        case [x, y]:
            return f"pair {x}, {y}"
        case [1, *rest]:
            return f"starts with 1, rest={rest}"
        case _:
            return "something else"

print(describe([]))           # empty
print(describe([42]))         # single element 42
print(describe([1, 2, 3, 4])) # starts with 1, rest=[2, 3, 4]
```

## 클래스와 매핑 패턴

클래스는 `__match_args__` 속성을 정의하여 패턴 매칭 시 사용할 위치 속성을 지정할 수 있습니다. 매핑 패턴은 딕셔너리에서 지정된 키만 일치시키며, 일치하지 않은 키는 무시됩니다.

```python
class Point:
    __match_args__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x; self.y = y

p = Point(1, 2)
match p:
    case Point(x, y):
        print("point at", x, y)

match {"kind": "circle", "radius": 3}:
    case {"kind": "circle", "radius": r}:
        print("circle of radius", r)
```

## OR 패턴과 가드

`|` 연산자를 사용하면 여러 패턴 중 하나에 일치시킬 수 있습니다. 패턴 뒤에 `if`를 추가하여 가드 표현식으로 조건을 적용할 수 있습니다.

```python
def classify(x):
    match x:
        case 0 | 1:
            return "small"
        case n if n > 100:
            return "large"
        case _:
            return "medium"
```

## 요약

구조적 패턴 매칭을 사용하면 시퀀스, 매핑, 클래스 패턴, OR 패턴, 가드 등을 통해 데이터를 간결하게 분해하고 분류할 수 있습니다【372741329340159†L101-L116】. 이 기능을 활용하여 복잡한 조건 분기를 선언적으로 표현해 보세요.