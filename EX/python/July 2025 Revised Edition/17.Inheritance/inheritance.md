---

# 상속과 다형성

## 상속

- 상속은 기존 클래스(부모 클래스)의 속성과 메서드를 새로운 클래스(자식 클래스)가 물려받아 재사용하는 기능입니다.
- 자식 클래스는 `class Child(Parent):` 형태로 선언합니다.

```python
class Animal:
    def speak(self):
        print("동물이 소리를 냅니다.")

class Dog(Animal):
    def speak(self):
        print("멍멍!")

a = Animal()
d = Dog()
a.speak()  # 동물이 소리를 냅니다.
d.speak()  # 멍멍!
```

## super() 함수

- 자식 클래스에서 부모 클래스의 메서드를 호출해야 할 때 `super()`를 사용합니다.

```python
class Cat(Animal):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def speak(self):
        super().speak()
        print(f"{self.name}: 야옹!")
```

## 다형성

- 다형성은 동일한 인터페이스를 사용하는 여러 클래스가 서로 다른 동작을 수행할 수 있는 성질입니다.
- 부모 클래스로 정의한 메서드를 자식 클래스에서 재정의(오버라이딩)함으로써 구현됩니다.

```python
def animal_sound(animal: Animal):
    animal.speak()

animal_sound(a)
animal_sound(d)
```

위 예제에서 `animal_sound()` 함수는 `Animal` 타입을 인자로 받지만, 실제로 전달된 객체가 어떤 타입인지에 따라 적절한 `speak()` 구현이 호출됩니다.

## 요약

상속을 사용하면 코드 재사용성을 높일 수 있고, 다형성을 통해 공통 인터페이스를 유지하면서 다양한 동작을 구현할 수 있습니다. `super()`로 부모 클래스의 기능을 확장하고, 메서드 오버라이딩을 통해 자식 클래스만의 동작을 정의하세요.

## 추가 설명

### 다중 상속과 MRO

파이썬은 다중 상속을 지원하므로 하나의 클래스가 여러 부모 클래스를 상속받을 수 있습니다. 이때 메서드 탐색 순서는 **MRO(Method Resolution Order)**에 의해 결정됩니다. MRO는 C3 linearization 알고리즘을 사용하며, `클래스.__mro__` 속성으로 확인할 수 있습니다. 다중 상속은 복잡성을 증가시키므로, mixin 패턴처럼 기능을 작은 단위로 분리하는 경우에만 사용하는 것이 좋습니다.

```python
class A:
    def who(self):
        print('A')

class B(A):
    def who(self):
        print('B')

class C(A):
    def who(self):
        print('C')

class D(B, C):
    pass

d = D()
d.who()  # MRO에 따라 B가 먼저 호출됨
print(D.__mro__)
```

### 추상 클래스와 인터페이스

`abc` 모듈의 `ABC`와 `abstractmethod`를 이용하면 추상 베이스 클래스를 정의할 수 있습니다. 추상 클래스는 공통 인터페이스를 강제하고, 자식 클래스가 구현해야 할 메서드를 명시합니다.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14 * self.r * self.r

circle = Circle(2)
print(circle.area())
```

### super() 호출 순서

`super()`는 단일 상속뿐만 아니라 다중 상속에서도 올바른 MRO에 따라 상위 메서드를 호출합니다. 따라서 다중 상속을 사용하는 경우에도 `super()`를 일관되게 호출하는 것이 중요합니다.