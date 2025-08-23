# print.py
# print 함수 예제

# 1. 기본 출력
print("Hello, World!")   # 문자열
print(123)               # 정수
print(3.14)              # 실수
print(True)              # 불리언
print([1, 2, 3])         # 리스트
print({"key": "value"})  # 딕셔너리
print((1, 2, 3))         # 튜플
print(None)              # None

print("-" * 30)  # 구분선

# 2. 여러 값 출력
print("오늘은", 2, "장")  # 공백으로 구분됨

# 3. sep 옵션 (separator)
print("2025", "08", "21", sep="-")   # 2025-08-21
print("python", "is", "fun", sep="💡")

# 4. end 옵션
print("Hello", end=" ")
print("World")  # 줄바꿈 대신 공백으로 이어짐

# 5. file 옵션 (출력 내용을 파일로 저장)
with open("output.txt", "w") as f:
    print("이 문장은 콘솔이 아닌 파일에 기록됩니다.", file=f)

# 6. flush 옵션 (출력을 즉시 화면에 반영)
import time
for i in range(3):
    print(i, end=" ", flush=True)
    time.sleep(1)
