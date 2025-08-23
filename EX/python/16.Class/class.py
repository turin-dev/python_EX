# 클래스와 객체 예제

# 기본 클래스 정의
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"안녕하세요, 저는 {self.name}이고 {self.age}살입니다.")


# 데이터 클래스 사용 예제
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float


if __name__ == "__main__":
    p = Person("투린", 14)
    p.greet()
    p1 = Point(1.0, 2.0)
    print('Point instance:', p1)

    # 클래스 속성과 인스턴스 속성 예제
    class Counter:
        count = 0
        def __init__(self):
            Counter.count += 1
            self.id = Counter.count

    a = Counter(); b = Counter()
    print('Counter ids:', a.id, b.id, 'count:', Counter.count)

    # 클래스 메서드와 정적 메서드 예제
    class Math:
        @staticmethod
        def add(a, b):
            return a + b
        @classmethod
        def identity(cls):
            return cls()

    print('Math.add:', Math.add(3, 4))
    print('Math.identity instance:', isinstance(Math.identity(), Math))

    # 캡슐화 예제
    class Secret:
        def __init__(self):
            self._hint = '비공개'
            self.__secret = '진짜 비밀'

    s = Secret()
    print('hint:', s._hint)
    print('secret via mangled name:', s._Secret__secret)

    # property 사용 예제
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

    temp = Temperature(25)
    print('temperature:', temp.celsius)
    temp.celsius = 30
    print('temperature after set:', temp.celsius)