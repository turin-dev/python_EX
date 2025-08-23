# 람다와 고차 함수 예제

# 람다를 이용한 제곱 함수
square = lambda x: x * x
print('square(5):', square(5))

# 고차 함수 예제: map, filter, reduce
from functools import reduce

numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
product = reduce(lambda x, y: x * y, numbers)

print('squares:', squares)
print('evens:', evens)
print('product:', product)

# 람다보다 리스트 컴프리헨션이 더 간결한 예
words = ['Python', 'Java', 'C']
lengths_lambda = list(map(len, words))
lengths_comprehension = [len(w) for w in words]

print('lengths using map:', lengths_lambda)
print('lengths using comprehension:', lengths_comprehension)

# 람다를 정렬의 키 함수로 사용
words = ['apple', 'Banana', 'cherry']
print('sorted ignore case:', sorted(words, key=lambda w: w.lower()))

# any와 all 함수와 람다
numbers2 = [2, 4, 6, 7]
all_even = all(map(lambda x: x % 2 == 0, numbers2))
any_odd = any(map(lambda x: x % 2 == 1, numbers2))
print('all even:', all_even, 'any odd:', any_odd)

# functools.partial 사용
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print('square(5):', square(5), 'cube(2):', cube(2))