# 딕셔너리와 집합 예제

# 딕셔너리 생성과 수정
person = {"name": "투린", "age": 14}
print('name:', person["name"])
person["age"] = 15
person["city"] = "포항"

for key, value in person.items():
    print(key, value)

# 딕셔너리 기타 메서드 예제
print('city (default unknown):', person.get('city', 'unknown'))
person.setdefault('city', '포항')
print('city after setdefault:', person['city'])

removed_age = person.pop('age')  # pop은 키를 제거하고 값 반환
print('removed age:', removed_age)
del person['city']
print('after deletion:', person)

# 집합 연산 추가 예제
print('is subset:', {1, 2} <= a)
print('is superset:', a >= {1, 2})

fs = frozenset([1, 2])
print('frozenset:', fs)
squares_set = {x*x for x in range(5)}
print('squares_set:', squares_set)

# 딕셔너리 컴프리헨션
squares = {x: x**2 for x in range(5)}
print('squares dict:', squares)

# 집합 연산 예제
a = {1, 2, 3}
b = {2, 3, 4}
print('union:', a | b)
print('intersection:', a & b)
print('difference:', a - b)
print('symmetric difference:', a ^ b)