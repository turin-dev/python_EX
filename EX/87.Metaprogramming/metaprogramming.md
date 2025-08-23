# 제87장 – 메타프로그래밍: 메타클래스와 디스크립터

메타프로그래밍은 코드를 조작하는 코드를 작성하는 기술입니다. 파이썬에서는 메타클래스, 디스크립터 및 특수 메서드를 사용하여 객체의 동작을 런타임에 맞춤화할 수 있습니다. 언어 참조는 `__getattr__()`와 `__setattr__()`를 정의해 속성 접근을 사용자 정의하는 방법과【271779506080093†L1761-L1774】, `__add__`와 `__mul__`과 같은 연산자 메서드가 어떻게 구현되는지를 설명합니다【271779506080093†L2634-L2666】.

## 디스크립터

디스크립터는 `__get__`, `__set__`, `__delete__` 중 하나 이상의 메서드를 정의하는 객체입니다. 다른 객체의 속성으로 접근될 때 이 메서드들이 호출되어 접근을 제어합니다. 디스크립터는 프로퍼티, 메서드, 클래스 변수의 기본 동작을 구현하며, 계산된 속성이나 검증, 위임을 수행하는 데 사용됩니다.

```python
class IntegerField:
    def __init__(self):
        self._value = 0
    def __get__(self, instance, owner):
        return self._value
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Expected int")
        self._value = value

class Point:
    x = IntegerField()
    y = IntegerField()

p = Point()
p.x = 10  # IntegerField.__set__ 호출
print(p.x)  # IntegerField.__get__ 호출, 10 출력
```

## 메타클래스

메타클래스는 클래스의 클래스입니다. 클래스가 생성되는 방식을 제어할 수 있습니다. 커스텀 메타클래스를 정의하려면 `type`을 상속하고 `__new__()`나 `__init__()`을 구현합니다. 클래스 정의 시 `metaclass=YourMeta`를 지정합니다. 메타클래스는 클래스 속성을 수정하거나 클래스 레지스트리를 생성하는 데 사용할 수 있습니다.

```python
class RegistryMeta(type):
    registry = {}
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        RegistryMeta.registry[name] = cls
        return cls

class Base(metaclass=RegistryMeta):
    pass

class PluginA(Base):
    pass
class PluginB(Base):
    pass

print(RegistryMeta.registry)  # {'Base': <class ...>, 'PluginA': <class ...>, 'PluginB': <class ...>}
```

## 요약

메타프로그래밍을 통해 디스크립터로 속성 접근을 제어하고, 메타클래스로 클래스 생성 로직을 변경할 수 있습니다. 이러한 기법은 제약을 enforced 하거나, 클래스 레지스트리를 구축하거나, 도메인 특화 언어를 구현하는 데 유용합니다. `__getattr__` 같은 특수 메서드와 연산자 오버로딩을 이해하면 객체 동작을 세밀하게 제어할 수 있습니다【271779506080093†L1761-L1774】【271779506080093†L2634-L2666】.