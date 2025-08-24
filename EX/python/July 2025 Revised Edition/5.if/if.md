

---

# 5장. 조건문 (if문)

## 조건문이란?

조건(참/거짓)에 따라 코드의 실행 흐름을 제어하는 구문입니다.

* 조건이 `True`면 실행
* 조건이 `False`면 실행하지 않음

---

## 1. 기본 if문

```python
if 조건식:
    실행할 코드
```

✔ 조건식이 참일 때만 코드 실행

```python
x = 10
if x > 5:
    print("x는 5보다 큽니다.")
```

---

## 2. if \~ else문

```python
if 조건식:
    실행할 코드1
else:
    실행할 코드2
```

✔ 조건에 따라 두 가지 중 하나 실행

```python
age = 14
if age >= 18:
    print("성인입니다.")
else:
    print("미성년자입니다.")
```

---

## 3. if \~ elif \~ else문

```python
if 조건1:
    실행1
elif 조건2:
    실행2
else:
    실행3
```

✔ 여러 조건 중 하나만 선택 실행

```python
score = 85
if score >= 90:
    print("A 학점")
elif score >= 80:
    print("B 학점")
else:
    print("C 학점 이하")
```

---

## 4. 중첩 if문

if문 안에 if문을 또 넣을 수 있습니다.

```python
num = 12
if num > 0:
    if num % 2 == 0:
        print("양수이면서 짝수입니다.")
```

---

## 5. 조건 표현식 (삼항 연산자)

한 줄로 if \~ else 표현

```python
결과 = 값1 if 조건 else 값2
```

```python
y = 20
result = "짝수" if y % 2 == 0 else "홀수"
print(result)
```

---

📌 정리

* **if** : 조건이 참이면 실행
* **if \~ else** : 조건에 따라 둘 중 하나 실행
* **if \~ elif \~ else** : 여러 조건 중 하나 선택
* **중첩 if** : 조건문 안의 조건문
* **조건 표현식** : 한 줄로 간단하게

---

