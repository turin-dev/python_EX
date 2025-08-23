# 제86장 – 파이썬의 디자인 패턴

디자인 패턴은 소프트웨어 설계에서 반복되는 문제에 대한 재사용 가능한 해결책입니다. 파이썬에서는 일급 함수, 클로저, 동적 타이핑 덕분에 많은 패턴이 간결하게 표현됩니다. 예를 들어, 데코레이터는 함수를 수정하거나 확장할 때 코드 자체를 변경하지 않고 기능을 추가할 수 있게 해 줍니다. 용어집에서는 데코레이터를 또 다른 함수를 반환하는 함수로 정의하며, `@decorator` 구문이 `f = decorator(f)`와 동등한 문법적 설탕임을 설명합니다【212515192382289†L370-L395】. 이 장에서는 파이썬으로 표현한 몇 가지 흔한 패턴을 살펴봅니다.

## 싱글턴 패턴

싱글턴 패턴은 클래스가 오직 하나의 인스턴스만 갖도록 하고 전역 접근점을 제공합니다. 파이썬에서는 `__new__()` 메서드를 재정의하거나, 모듈 자체를 싱글턴으로 사용하여 구현할 수 있습니다. 아래는 클래스 속성에 인스턴스를 저장하는 간단한 구현입니다.

```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton(); b = Singleton()
print(a is b)  # True
```

## 옵저버 패턴

옵저버 패턴은 객체(옵저버)가 다른 객체(주체)의 상태 변화에 대해 통지받을 수 있도록 합니다. 주체의 상태가 변경되면 모든 옵저버에게 알립니다. 파이썬에서는 콜백이나 `asyncio` 이벤트 루프를 사용해 이 패턴을 구현할 수 있습니다.

```python
class Observable:
    def __init__(self):
        self._observers = []
    def subscribe(self, observer):
        self._observers.append(observer)
    def notify(self, message):
        for obs in self._observers:
            obs.update(message)

class Observer:
    def update(self, message):
        print("Received:", message)

subject = Observable()
obs1 = Observer(); obs2 = Observer()
subject.subscribe(obs1); subject.subscribe(obs2)
subject.notify("Hello observers!")
```

## 팩토리 패턴

팩토리 패턴은 객체 생성 로직을 캡슐화합니다. 간단한 팩토리 함수나 클래스 메서드가 입력에 따라 어떤 클래스를 인스턴스화할지 결정합니다.

```python
class Animal:
    def speak(self) -> str:
        raise NotImplementedError

class Cat(Animal):
    def speak(self) -> str:
        return "meow"

class Dog(Animal):
    def speak(self) -> str:
        return "woof"

def animal_factory(kind: str) -> Animal:
    if kind == 'cat': return Cat()
    elif kind == 'dog': return Dog()
    else: raise ValueError("Unknown animal")

animal = animal_factory('cat')
print(animal.speak())  # meow
```

## 요약

싱글턴, 옵저버, 팩토리와 같은 디자인 패턴은 파이썬에서 간결하게 표현할 수 있습니다. 데코레이터는 정의 시 함수나 클래스를 수정하는 내장 기능으로, 메모이제이션이나 등록 패턴과 같은 패턴을 구현하는 데 유용합니다【212515192382289†L370-L395】. 이러한 패턴을 이해하면 코드를 재사용 가능하고 유연하게 구조화하는 데 도움이 됩니다.