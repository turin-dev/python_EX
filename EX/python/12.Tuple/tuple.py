# 튜플 예제

# 튜플 생성과 인덱싱
coords = (10, 20)
print('coords[0]:', coords[0])

# 튜플은 불변 - 아래 줄의 주석을 해제하면 TypeError 발생
# coords[0] = 99

# 언패킹(unpacking)
x, y = coords
print('x:', x, 'y:', y)

# 한 요소 튜플 생성
singleton = (42,)
print('singleton:', singleton, 'type:', type(singleton))

# 튜플 메서드와 활용
numbers = (1, 2, 2, 3)
print('count of 2:', numbers.count(2))
print('index of 3:', numbers.index(3))

# 가변 길이 언패킹
head, *tail = (1, 2, 3, 4)
print('head:', head, 'tail:', tail)

# namedtuple 사용 예제
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print('namedtuple Point:', p, 'x:', p.x, 'y:', p.y)