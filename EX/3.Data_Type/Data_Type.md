
---

# 자료형 (Data Type)

## 자료형이란?

* **데이터의 종류를 구분하는 방법**
* 파이썬은 값을 넣을 때 자동으로 자료형을 결정한다. (동적 타입 언어)

---

## 1. 숫자형 (Numeric Type)

* **정수(int)** : 소수점 없는 수
* **실수(float)** : 소수점 있는 수
* **복소수(complex)** : 실수부 + 허수부

```python
a = 10       # int
b = 3.14     # float
c = 2 + 3j   # complex

print(type(a))  # <class 'int'>
print(type(b))  # <class 'float'>
print(type(c))  # <class 'complex'>
```

---

## 2. 문자열 (String, `str`)

* `" "` 또는 `' '` 안에 문자/단어/문장을 표현
* 여러 줄 문자열은 `""" """` 또는 `''' '''`

```python
s1 = "Hello"
s2 = 'Python'
s3 = """여러 줄
문자열"""

print(s1, s2)
print(s3)
```

---

## 3. 불리언 (Boolean, `bool`)

* `True`, `False` 두 값만 존재
* 주로 조건문에서 사용

```python
is_student = True
is_teacher = False
print(is_student, is_teacher)
```

---

## 4. 자료구조형 (Collection Types)

여러 값을 한꺼번에 담는 자료형

### 리스트 (list)

* 순서 있음, 값 변경 가능

```python
numbers = [1, 2, 3, 4]
numbers[0] = 10
print(numbers)  # [10, 2, 3, 4]
```

### 튜플 (tuple)

* 순서 있음, 값 변경 불가

```python
coords = (10, 20)
# coords[0] = 99  # 에러 발생
print(coords)
```

### 딕셔너리 (dict)

* 키(key)와 값(value) 쌍으로 저장

```python
person = {"name": "투린", "age": 14}
print(person["name"])
```

### 집합 (set)

* 중복 허용 안 함, 순서 없음

```python
s = {1, 2, 2, 3}
print(s)  # {1, 2, 3}
```

---

## 5. None

* "값이 없음"을 의미하는 특별한 자료형

```python
x = None
print(x)       # None
print(type(x)) # <class 'NoneType'>
```

---

👉 요약하면:

* **단일 값**: int, float, complex, str, bool, None
* **여러 값**: list, tuple, dict, set

---

여기까지가 **3장 이론 정리**야.
실습용 `datatype.py` 파일을 만들어서 예제 코드를 실행하면 1\~2장처럼 바로 확인 가능해.

👉 내가 `datatype.py` 기본 코드 예제도 만들어줄까?
