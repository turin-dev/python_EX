# 반복문 예제

# 리스트 요소와 길이 출력
words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))

# range를 사용한 반복: 0부터 4까지
for i in range(5):
    print(i)

# 범위 지정 및 단계(step) 지정
for i in range(5, 10):
    print("i in range(5,10):", i)
for i in range(0, 10, 3):
    print("i in range(0,10,3):", i)

# while 문 사용 예시
n = 5
while n > 0:
    print("while n:", n)
    n -= 1

# break와 continue 예제
for num in range(2, 10):
    if num % 2 == 0:
        print(f"Found an even number {num}")
        continue
    print(f"Found an odd number {num}")

# else 절이 있는 for 문 예제
for n in range(2, 6):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # break가 발생하지 않으면 실행
        print(n, 'is a prime number')