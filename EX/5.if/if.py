# condition.py
# 조건문 예제

print("=== 1. 기본 if문 ===")
x = 10
if x > 5:
    print("x는 5보다 큽니다.")

print("\n=== 2. if ~ else문 ===")
age = 14
if age >= 18:
    print("성인입니다.")
else:
    print("미성년자입니다.")

print("\n=== 3. if ~ elif ~ else문 ===")
score = 85
if score >= 90:
    print("A 학점")
elif score >= 80:
    print("B 학점")
else:
    print("C 학점 이하")

print("\n=== 4. 중첩 if문 ===")
num = 12
if num > 0:
    if num % 2 == 0:
        print("양수이면서 짝수입니다.")
    else:
        print("양수이면서 홀수입니다.")
else:
    print("0 또는 음수입니다.")

print("\n=== 5. 조건 표현식 (삼항 연산자) ===")
y = 20
result = "짝수" if y % 2 == 0 else "홀수"
print("y는", result)
