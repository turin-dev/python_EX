# datatype.py
# 자료형(Data Type) 예제

# 1. 숫자형
a = 10        # int
b = 3.14      # float
c = 2 + 3j    # complex

print("정수:", a, type(a))
print("실수:", b, type(b))
print("복소수:", c, type(c))

print("-" * 30)

# 2. 문자열
s1 = "Hello"
s2 = 'Python'
s3 = """여러 줄
문자열"""

print("문자열1:", s1)
print("문자열2:", s2)
print("문자열3:", s3)

print("-" * 30)

# 3. 불리언
is_student = True
is_teacher = False
print("불리언 값:", is_student, is_teacher)

print("-" * 30)

# 4. 자료구조

# 리스트 (순서 O, 변경 O)
numbers = [1, 2, 3, 4]
numbers[0] = 99
print("리스트:", numbers, type(numbers))

# 튜플 (순서 O, 변경 X)
coords = (10, 20)
print("튜플:", coords, type(coords))

# 딕셔너리 (key:value)
person = {"name": "투린", "age": 14}
print("딕셔너리:", person, type(person))
print("딕셔너리에서 name:", person["name"])

# 집합 (중복 X, 순서 X)
s = {1, 2, 2, 3}
print("집합:", s, type(s))

print("-" * 30)

# 5. None
x = None
print("None 값:", x, type(x))
