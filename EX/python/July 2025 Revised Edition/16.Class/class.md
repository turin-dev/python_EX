---

# 클래스와 객체

## 클래스란?

- 클래스는 관련된 데이터와 메서드를 한 곳에 묶는 사용자 정의 데이터 타입입니다.
- `class` 키워드로 정의하며, 클래스 내부에는 속성(변수)과 메서드(함수)를 정의합니다.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"안녕하세요, 저는 {self.name}이고 {self.age}살입니다.")

p = Person("투린", 14)
p.greet()
```

## self

- 인스턴스 메서드는 첫 번째 매개변수로 항상 `self`를 받으며, 이는 해당 객체 자체를 가리킵니다.
- 클래스 내부에서 속성에 접근하려면 `self.속성명` 형태를 사용합니다.

## 특수 메서드

- `__init__(self, ...)` : 객체 생성 시 호출되는 초기화 메서드입니다.
- `__str__(self)` : `str()`나 `print()` 함수가 객체를 문자열로 표현할 때 호출됩니다.
- 그 외에도 `__repr__`, `__len__` 등 여러 특수 메서드를 오버라이드할 수 있습니다.

## 데이터 클래스(dataclass)

- Python 3.7부터 제공되는 `dataclasses.dataclass` 데코레이터를 사용하면, 반복적인 초기화 코드 없이 간단한 데이터 보관용 클래스를 자동으로 생성할 수 있습니다.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
print(p1)  # Point(x=1.0, y=2.0)
```

## 요약

클래스는 객체 지향 프로그래밍의 기본 단위로, 데이터를 구조화하고 관련 동작을 정의할 수 있습니다. `self`를 통해 인스턴스 속성에 접근하며, `__init__`과 같은 특수 메서드를 이용해 객체의 동작을 제어합니다. `dataclass`를 사용하면 단순 데이터 객체를 손쉽게 정의할 수 있습니다.

## 추가 설명

### 클래스 속성과 인스턴스 속성

클래스 정의 내부에서 직접 할당된 변수는 모든 인스턴스가 공유하는 **클래스 속성**입니다. 반면 `self`를 통해 할당한 변수는 각 인스턴스마다 별도의 값을 갖는 **인스턴스 속성**입니다.

```python
class Counter:
    count = 0  # 클래스 속성
    def __init__(self):
        Counter.count += 1
        self.id = Counter.count  # 인스턴스 속성

a = Counter(); b = Counter()
print(a.id, b.id, Counter.count)  # 1 2 2
```

### 메서드 종류: 인스턴스, 클래스, 정적 메서드

일반 메서드는 첫 번째 인자로 `self`를 받아 인스턴스에 접근합니다. `@classmethod`가 붙은 메서드는 `cls`를 첫 인자로 받아 클래스를 수정하거나 생성자를 대체할 때 사용합니다. `@staticmethod`는 클래스와 인스턴스 어느 쪽에도 의존하지 않는 유틸리티 함수를 정의할 때 사용합니다.

```python
class Math:
    @staticmethod
    def add(a, b):
        return a + b
    @classmethod
    def identity(cls):
        return cls()
```

### 캡슐화와 속성 보호

파이썬에는 엄격한 접근 제한자가 없지만, 언더스코어 접두어 관례를 사용하여 외부 사용자가 속성에 직접 접근하지 않도록 힌트를 줄 수 있습니다. 이름 맹글링(name mangling)을 적용하려면 `__속성`과 같이 두 개의 밑줄을 사용합니다.

```python
class Secret:
    def __init__(self):
        self._hint = '비공개 (protected)'  # 관례상 보호 속성
        self.__secret = '진짜 비밀'       # name mangling

obj = Secret()
print(obj._hint)
# print(obj.__secret)  # AttributeError
print(obj._Secret__secret)  # name mangled 속성 접근
```

### 프로퍼티와 getter/setter

`@property` 데코레이터를 사용하면 메서드를 속성처럼 사용하여 계산된 값을 제공하고, `@속성.setter`를 통해 속성 할당 시 실행되는 로직을 정의할 수 있습니다. 이는 데이터 유효성을 검증하거나 읽기 전용 속성을 만들 때 유용합니다.

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius
    @property
    def celsius(self) -> float:
        return self._celsius
    @celsius.setter
    def celsius(self, value: float):
        if value < -273.15:
            raise ValueError('절대 영도 이하입니다!')
        self._celsius = value

t = Temperature(25)
print(t.celsius)
t.celsius = 30
```