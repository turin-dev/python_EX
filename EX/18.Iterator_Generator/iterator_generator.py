# 이터레이터와 제너레이터 예제

# 이터레이터 사용 예
it = iter([1, 2, 3])
print('next(it):', next(it))
print('next(it):', next(it))
print('next(it):', next(it))

# 제너레이터 함수 정의
def countdown(n):
    while n > 0:
        yield n
        n -= 1


# 제너레이터 사용 예
for i in countdown(3):
    print('countdown:', i)

# 제너레이터 표현식
squares = (x**2 for x in range(5))
for s in squares:
    print('square:', s)

# 사용자 정의 이터레이터 클래스
class CountDown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

print('CountDown:')
for num in CountDown(3):
    print(num)

# 제너레이터 send와 yield from 예제
def echo():
    received = None
    while True:
        received = yield received

gen = echo()
next(gen)
print('echo send hello:', gen.send('hello'))
print('echo send world:', gen.send('world'))

def nested():
    yield from range(3)
    yield from ['a', 'b']

print('nested list:', list(nested()))

# itertools 사용 예제
from itertools import chain, islice, cycle, product

print('chain:', list(chain('ab', 'cd')))
print('islice:', list(islice(range(10), 3, 6)))
print('cycle:', [(i, ch) for i, ch in zip(range(3), cycle('xy'))])
print('product:', list(product([1, 2], ['a', 'b'])))