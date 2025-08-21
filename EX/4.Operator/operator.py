# operator.py
# 연산자 예제

print("=== 1. 산술 연산자 ===")
a, b = 10, 3
print("a + b =", a + b)
print("a - b =", a - b)
print("a * b =", a * b)
print("a / b =", a / b)
print("a // b =", a // b)
print("a % b =", a % b)
print("a ** b =", a ** b)

print("\n=== 2. 비교 연산자 ===")
x, y = 5, 10
print("x == y:", x == y)
print("x != y:", x != y)
print("x > y:", x > y)
print("x < y:", x < y)
print("x >= y:", x >= y)
print("x <= y:", x <= y)

print("\n=== 3. 논리 연산자 ===")
p, q = True, False
print("p and q:", p and q)
print("p or q:", p or q)
print("not p:", not p)

print("\n=== 4. 대입 연산자 ===")
x = 10
print("초기 x:", x)
x += 5
print("x += 5 →", x)
x -= 3
print("x -= 3 →", x)
x *= 2
print("x *= 2 →", x)
x /= 4
print("x /= 4 →", x)

print("\n=== 5. 멤버십 연산자 ===")
nums = [1, 2, 3, 4]
print("3 in nums:", 3 in nums)
print("5 not in nums:", 5 not in nums)

print("\n=== 6. 아이덴티티 연산자 ===")
a = [1, 2, 3]
b = a
c = [1, 2, 3]
print("a is b:", a is b)      # 같은 객체
print("a is c:", a is c)      # 다른 객체
print("a == c:", a == c)      # 내용만 같음
