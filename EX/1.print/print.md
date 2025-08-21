
---

# print

## print 함수란?

Python에서 **콘솔(터미널)에 원하는 값을 출력**하는 내장 함수입니다.
프로그램이 어떤 결과를 내는지 확인할 때 가장 기본이 되는 도구입니다.

---

## print 함수 사용법

```python
print(출력할 내용, sep=' ', end='\n', file=sys.stdout, flush=False)
```

---

## print 함수 예시

```python
print("Hello, World!")   # 문자열 출력
print(123)               # 정수 출력
print(3.14)              # 실수 출력
print(True)              # 불리언 출력
print([1, 2, 3])         # 리스트 출력
print({"key": "value"})  # 딕셔너리 출력
print((1, 2, 3))         # 튜플 출력
print(None)              # None 출력
```

---

## print 함수 옵션

### 1. `sep` (separator)

출력할 값이 여러 개인 경우, **값 사이에 들어갈 문자열**을 지정합니다.
기본값은 `' '` (공백)입니다.

```python
print("2025", "08", "21", sep="-")
# 출력: 2025-08-21
```

---

### 2. `end`

출력 후에 **마지막에 덧붙일 문자열**을 지정합니다.
기본값은 `'\n'` (줄바꿈)입니다.

```python
print("Hello", end=" ")
print("World")
# 출력: Hello World
```

---

### 3. `file`

출력 결과를 **콘솔이 아니라 파일로 보내고 싶을 때** 사용합니다.
기본값은 `sys.stdout` (터미널 출력)입니다.

```python
with open("output.txt", "w") as f:
    print("파일에 기록됩니다!", file=f)
```

---

### 4. `flush`

출력할 내용을 **버퍼에 쌓지 않고 바로 출력할지 여부**를 결정합니다.
`True`로 설정하면 즉시 출력합니다. (실시간 로그 등에 유용)

```python
import time

for i in range(5):
    print(i, end=" ", flush=True)
    time.sleep(1)
# 1초마다 값이 출력됨
```

---

이 정도면 1장 `print`는 **실전 + 이론 풀패키지** 느낌으로 정리된 거야.
다음 챕터로는 보통 **변수**를 다루는데, `print`랑 바로 연결해서 설명하면 이해가 훨씬 쉬워져.

👉 내가 `print` + **변수** 연결해서 예제 만들어줄까?
