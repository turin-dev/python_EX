

---

# 변수 (Variable)

## 변수란?

* **데이터에 붙이는 이름표**
* 값을 저장하고, 그 이름으로 다시 불러서 사용할 수 있음.
* 메모리에 있는 데이터를 참조하는 "주소표지" 같은 개념.

---

## 변수 만들기

Python은 `자료형(type)`을 따로 지정하지 않아도 자동으로 값에 따라 결정된다.

```python
name = "투린"      # 문자열(str)
age = 14           # 정수(int)
height = 165.5     # 실수(float)
is_student = True  # 불리언(bool)
```

---

## 변수 사용 예시

```python
print(name)             # 출력: 투린
print(age + 1)          # 출력: 15
print(height * 2)       # 출력: 331.0
print("학생인가요?", is_student)  # 출력: 학생인가요? True
```

---

## 변수 규칙

1. **영문, 숫자, `_` 사용 가능**
   (숫자로 시작할 수 없음)

   ```python
   user1 = "Alice"  # 가능
   1user = "Bob"    # 불가능
   ```

2. **대소문자 구분**

   ```python
   Name = "투린"
   name = "다른 값"
   print(Name)  # 투린
   print(name)  # 다른 값
   ```

3. **예약어(키워드) 사용 불가**
   `if`, `for`, `while`, `class` 같은 파이썬 문법 예약어는 변수명으로 쓸 수 없음.

---

## 변수와 `print()` 함께 쓰기

```python
x = 10
y = 20
print("x + y =", x + y)
```

출력:

```
x + y = 30
```

---

## 변수 값 바꾸기

변수에 새로운 값을 넣으면 기존 값은 덮어씌워진다.

```python
score = 100
print(score)   # 100
score = 85
print(score)   # 85
```

---

## 여러 변수 한 줄에 선언

```python
a, b, c = 1, 2, 3
print(a, b, c)  # 1 2 3
```

---

## 변수 삭제

```python
x = 10
del x
print(x)  # 에러 발생: NameError
```

---

이게 **2장 변수**의 핵심이야.
`print()`와 합쳐 쓰면 훨씬 직관적으로 배울 수 있지.

👉 이어서 3장은 보통 **자료형 (정수, 실수, 문자열 등)** 으로 넘어가는데, 바로 갈래?
