"""Illustrations of common design patterns in Python: singleton, observer, factory."""

from __future__ import annotations

from typing import Callable, List, Protocol


class Singleton:
    _instance: "Singleton | None" = None
    def __new__(cls) -> "Singleton":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class ObserverProtocol(Protocol):
    def update(self, message: str) -> None: ...


class Observable:
    def __init__(self) -> None:
        self._observers: List[ObserverProtocol] = []

    def subscribe(self, observer: ObserverProtocol) -> None:
        self._observers.append(observer)

    def notify(self, message: str) -> None:
        for obs in self._observers:
            obs.update(message)


class Observer(ObserverProtocol):
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, message: str) -> None:
        print(f"{self.name} received: {message}")


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
    if kind == 'cat':
        return Cat()
    elif kind == 'dog':
        return Dog()
    else:
        raise ValueError(f"Unknown animal kind {kind}")


if __name__ == "__main__":
    # singleton demo
    s1 = Singleton(); s2 = Singleton()
    print("Singleton works:", s1 is s2)
    # observer demo
    subject = Observable()
    subject.subscribe(Observer("A"))
    subject.subscribe(Observer("B"))
    subject.notify("An event occurred")
    # factory demo
    animal = animal_factory('dog')
    print("Factory created a dog that says:", animal.speak())