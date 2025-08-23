# 32. 타입 힌트와 `typing` 모듈

파이썬은 동적 타입 언어지만, **타입 힌트(type hint)**를 통해 변수와 함수의 타입을 명시할 수 있다. 문서에서는 **런타임에서 타입 힌트가 강제되지 않으며, 정적 분석 도구와 IDE가 이를 사용해 오류를 발견하도록 돕는다**고 설명한다【678476496501786†L86-L110】. 타입 힌트는 코드 가독성을 높이고 자동 완성 기능을 개선한다.

## 기본 문법

- 변수: `age: int = 30`
- 함수 인자와 반환값: `def greet(name: str) -> str:`
- 컨테이너 타입: `list[int]`, `dict[str, float]`, `set[str]`
- 선택적 값: `from typing import Optional`; `price: Optional[float] = None`
- 여러 타입 중 하나: `from typing import Union`; `data: Union[str, bytes]`

```python
def surface_area_of_cube(length: float) -> float:
    return 6 * (length ** 2)

print(surface_area_of_cube(3.0))
```

위 예제는 숫자를 인자로 받아 부동소수점 결과를 반환한다. 문서는 이런 주석들이 **정적 타입 검사기(예: mypy)**가 분석할 수 있게 해 주며, 런타임에는 아무런 영향을 주지 않는다고 명시한다【678476496501786†L86-L110】.

## `typing` 모듈의 고급 타입

`typing` 모듈은 더 복잡한 타입을 표현하기 위한 도구를 제공한다.

- `TypedDict`: 딕셔너리의 키와 값 타입을 지정한다.
- `Protocol`: 특정 메서드 집합을 가진 객체를 정의하여 구조적 서브타이핑을 지원한다.
- `Literal`: 리터럴 값 몇 개만 허용하는 타입을 지정한다.
- `Final`: 변수나 속성을 상수로 표시한다.
- `Annotated`: 타입과 함께 메타데이터를 첨부한다.

예를 들어:

```python
from typing import TypedDict, Literal, Protocol, Iterable

class Point(TypedDict):
    x: float
    y: float

def draw_point(pt: Point) -> None:
    print(f"Point({pt['x']}, {pt['y']})")

class SupportsLen(Protocol):
    def __len__(self) -> int: ...

def show_length(x: SupportsLen) -> None:
    print(len(x))

Mode = Literal['r', 'w', 'a']

def open_file(path: str, mode: Mode) -> None:
    ...
```

## 타입 힌트와 런타임

타입 주석은 `__annotations__` 딕셔너리에 저장되며, `typing.get_type_hints()` 함수로 해석할 수 있다. 예를 들어 함수나 클래스의 주석을 검사하여 동적으로 타입 검사를 수행하는 라이브러리를 만들 수 있다. 하지만 문서에서 강조하듯 **파이썬 런타임은 주석을 해석하지 않고, 타입 힌트는 정적 분석 도구를 위한 정보일 뿐**이다【678476496501786†L86-L110】.

타입 힌트를 적극적으로 사용하면 복잡한 코드베이스에서 인터페이스를 명확히 정의하고 잠재적 버그를 줄일 수 있다.