# 제84장 – 고급 데이터 클래스

데이터 클래스는 PEP 557에서 도입되었으며, 타입 어노테이션을 기반으로 `__init__()`, `__repr__()`, `__eq__()` 같은 특수 메서드를 자동으로 생성합니다. `dataclasses` 모듈을 사용하면 생성되는 코드와 동작을 세밀하게 제어할 수 있습니다. 데이터 클래스는 보일러플레이트 코드를 줄이고 클래스를 더 선언적으로 만들 수 있게 해 줍니다【15749301015174†L65-L96】.

## 필드 옵션

* `default`와 `default_factory` – 필드의 기본값을 설정합니다. 기본값이 가변 객체(예: 리스트)일 경우 여러 인스턴스가 같은 객체를 공유하지 않도록 `default_factory`를 사용하세요.
* `init=False` – 해당 필드를 생성된 `__init__()` 메서드의 인자에서 제외합니다.
* `repr=False` – 해당 필드를 자동 생성되는 `__repr__()` 문자열에서 제외합니다.
* `compare=False` – 비교 메서드에서 필드를 제외합니다.
* `kw_only=True` – 필드를 키워드 인자로만 전달하도록 요구합니다.

## 클래스 옵션

* `frozen=True` – 데이터 클래스를 불변으로 만들어 모든 필드를 읽기 전용으로 만듭니다.
* `order=True` – `__eq__()` 외에도 `__lt__`, `__le__` 등의 순서 비교 메서드를 생성합니다.
* `slots=True` – `__slots__`를 사용하여 메모리 사용량을 줄이고 새 속성 추가를 방지합니다.

## 초기화 이후 처리

생성된 `__init__()` 이후 추가 초기화가 필요하다면 `__post_init__(self)` 메서드를 정의합니다. 이 메서드는 필드 검증이나 파생 속성 계산에 유용합니다.

## 예제

```python
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True, slots=True)
class Product:
    name: str
    price: float
    tags: list[str] = field(default_factory=list, repr=False)

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price must be non‑negative")

p = Product(name="Widget", price=9.99, tags=["sale"])
print(p)
```

## 요약

데이터 클래스는 보일러플레이트 코드를 자동으로 생성하며, 필드와 클래스 옵션을 통해 행동을 맞춤 설정할 수 있습니다【15749301015174†L65-L96】. `default_factory`, `frozen`, `order`, `slots` 등의 옵션을 사용해 세밀하게 제어하고, `__post_init__()`에서 추가 초기화나 검증을 수행하세요.