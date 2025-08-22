# 패턴 매칭 예제

# 기본 match 사용
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"


# 튜플 패턴 매칭
def describe_point(point):
    match point:
        case (0, 0):
            return "원점"
        case (0, y):
            return f"Y={y}"
        case (x, 0):
            return f"X={x}"
        case (x, y):
            return f"X={x}, Y={y}"
        case _:
            return "기타"


# 클래스 정의
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# 클래스 패턴 매칭 함수
def where_is(p):
    match p:
        case Point(x=0, y=0):
            return "원점"
        case Point(x=0, y=y):
            return f"Y={y}"
        case Point(x=x, y=0):
            return f"X={x}"
        case Point():
            return "기타"
        case _:
            return "점이 아님"


if __name__ == "__main__":
    # 기본 match 예제 호출
    print(http_error(404))
    # 튜플 패턴 매칭 호출
    print(describe_point((0, 5)))
    # 클래스 패턴 매칭 호출
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    p3 = Point(0, 3)
    print(where_is(p1))
    print(where_is(p2))
    print(where_is(p3))

    # 별표 패턴 예제
    def describe(seq):
        match seq:
            case []:
                return '빈 시퀀스'
            case [x]:
                return f'한 요소: {x}'
            case [first, *rest]:
                return f'첫 요소: {first}, 나머지: {rest}'
            case _:
                return '시퀀스 아님'

    print('describe:', describe([1, 2, 3]))

    # 매핑 패턴과 가드 예제
    def price(info):
        match info:
            case {'item': item, 'price': p} if p > 100:
                return f'{item} is expensive'
            case {'item': item, 'price': p}:
                return f'{item} costs {p}'
            case _:
                return '알 수 없는 정보'

    print('price:', price({'item': 'pen', 'price': 50}))

    # __match_args__ 사용 예제
    class Point3D:
        __match_args__ = ('x', 'y', 'z')
        def __init__(self, x, y, z):
            self.x, self.y, self.z = x, y, z

    p3d = Point3D(1, 2, 3)
    match p3d:
        case Point3D(x, y, z):
            print('Point3D:', x, y, z)