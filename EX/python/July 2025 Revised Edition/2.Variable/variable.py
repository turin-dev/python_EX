# variable.py
# 변수 예제

# 1. 기본 자료형 변수
name = "투린"       # 문자열
age = 14            # 정수
height = 165.5      # 실수
is_student = True   # 불리언

print("이름:", name)
print("나이:", age)
print("키:", height)
print("학생 여부:", is_student)

# 2. 자료구조 변수
numbers = [1, 2, 3]               # 리스트
person = {"name": "투린", "age": 14}  # 딕셔너리
coords = (10, 20)                 # 튜플
unique_numbers = {1, 2, 3, 3}     # 집합 (중복 제거됨)

print("리스트:", numbers)
print("딕셔너리:", person)
print("튜플:", coords)
print("집합:", unique_numbers)

# 3. 변수 값 변경
score = 100
print("초기 점수:", score)
score = 85
print("변경된 점수:", score)

# 4. 여러 변수 한 줄에 선언
a, b, c = 1, 2, 3
print("여러 변수:", a, b, c)

# 5. 전역/지역 변수 예시
x = 10  # 전역 변수

def example():
    y = 5  # 지역 변수
    print("함수 안:", x, y)

example()
print("함수 밖:", x)
# print(y)  # 에러! y는 함수 안에서만 존재
