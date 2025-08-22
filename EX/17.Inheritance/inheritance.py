# 상속과 다형성 예제

class Animal:
    def speak(self):
        print("동물이 소리를 냅니다.")


class Dog(Animal):
    def speak(self):
        print("멍멍!")


class Cat(Animal):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def speak(self):
        super().speak()
        print(f"{self.name}: 야옹!")


def animal_sound(animal: Animal):
    animal.speak()


if __name__ == "__main__":
    a = Animal()
    d = Dog()
    c = Cat("나비")
    animal_sound(a)
    animal_sound(d)
    animal_sound(c)

    # 다중 상속과 MRO 예제
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

    d_obj = D()
    d_obj.who()  # B가 호출됨
    print('MRO of D:', D.__mro__)

    # 추상 클래스 예제
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
    print('circle area:', circle.area())