---

# 문자열 다루기

## 문자열 생성과 인덱싱

- 큰따옴표(`""`)나 작은따옴표(`''`)로 묶어서 문자열을 생성합니다.
- 문자열은 시퀀스 타입이므로 인덱싱과 슬라이싱을 통해 문자에 접근할 수 있습니다.

```python
s = "Hello, Python"
print(s[0])    # H
print(s[7:])   # Python
```

## 문자열 메서드

- `strip()` : 양쪽 공백 제거
- `upper()`, `lower()` : 대소문자 변환
- `replace(old, new)` : 문자열 치환
- `split(sep=None)` : 구분자로 분리하여 리스트 반환

```python
text = "  Python is Fun!  "
print(text.strip().lower())  # "python is fun!"
print(text.replace("Fun", "Great"))
```

## 포맷팅: f‑문자열

- `f"{표현식}"` 형태로 문자열 안에 표현식을 삽입할 수 있습니다.
- Python 3.6에서 도입되었으며 3.12부터는 중괄호 안에서 더 유연하게 표현할 수 있습니다【385620794081796†L109-L127】.

```python
name = "투린"
age = 14
print(f"{name}의 나이는 {age}살입니다.")
# 3.12에서는 이스케이프가 복잡한 표현식도 허용됩니다.
```

## 멀티라인 문자열

- 세 개의 작은따옴표(`'''`)나 큰따옴표(`"""`)를 사용하여 여러 줄의 문자열을 작성할 수 있습니다.

```python
text = """여러 줄
문자열 예시"""
print(text)
```

## 문자열은 불변

- 문자열은 변경 불가능(immutable)하므로, 변경이 필요할 경우 새로운 문자열을 만들어야 합니다.

```python
s = "hello"
# s[0] = 'H'  # 오류 발생
s = 'H' + s[1:]
print(s)  # Hello
```

## 요약

문자열은 다양한 메서드와 포맷팅 기능을 제공하는 중요한 자료형입니다. f‑문자열을 활용하면 가독성 높은 문자열을 쉽게 작성할 수 있으며, Python 3.12에서 더욱 유연한 사용이 가능해졌습니다.

## 추가 설명과 고급 기능

### 검색과 카운팅

문자열에서 특정 부분 문자열을 찾기 위해 `find()`와 `index()` 메서드를 사용할 수 있습니다. `find()`는 발견한 위치의 인덱스를 반환하거나 찾지 못하면 `-1`을 반환하고, `index()`는 찾지 못하면 `ValueError`를 발생시킵니다. `count()`는 부분 문자열의 출현 횟수를 반환합니다.

```python
s = "banana"
print(s.find('an'))   # 1
print(s.count('a'))   # 3
```

또한 `startswith()`와 `endswith()`는 접두사나 접미사를 검사하는 데 유용합니다.

### 분할과 결합

`split()`은 구분자를 기준으로 문자열을 분할하여 리스트를 반환하고, `rsplit()`은 오른쪽부터 분할합니다. `splitlines()`는 줄바꿈 문자로 분할합니다. `join()`은 리스트의 문자열을 하나로 결합할 때 사용합니다.

```python
csv = "a,b,c"
fields = csv.split(',')
print(fields)  # ['a', 'b', 'c']

joined = '-'.join(fields)
print(joined)  # 'a-b-c'

lines = "line1\nline2".splitlines()
print(lines)  # ['line1', 'line2']
```

### 정렬과 채우기

문자열을 좌우로 정렬하거나 특정 길이로 채우기 위해 `ljust()`, `rjust()`, `center()`, `zfill()`을 사용할 수 있습니다. 특히 `zfill()`은 숫자 문자열 앞을 0으로 채워 고정 길이 숫자를 만들 때 유용합니다.

```python
n = '42'
print(n.zfill(5))    # '00042'
print('Hi'.center(10, '*'))  # '****Hi****'
```

### `format()` 메서드와 포맷 문자열

f-문자열 이전에는 `str.format()` 메서드가 널리 사용되었습니다. 중괄호 `{}` 안에 인덱스나 키워드를 지정하여 변수 값을 삽입합니다.

```python
template = "{name} scored {score:.2f} points"
print(template.format(name='투린', score=97.5))
```

### 바이트 문자열과 인코딩

문자열은 유니코드 문자 시퀀스입니다. 바이너리 데이터를 다룰 때는 `b'...'` 형식의 바이트 문자열을 사용하며, 텍스트를 파일에 저장하거나 네트워크로 전송할 때는 적절한 인코딩을 지정해야 합니다.

```python
data = '파이썬'.encode('utf-8')  # 문자열을 바이트로 인코딩
text = data.decode('utf-8')     # 바이트를 다시 문자열로 디코딩
```

## 참고

문자열은 변경 불가능하므로, 많은 문자열을 연결할 때 `join()`을 사용하는 것이 반복적인 `+=`보다 효율적입니다. 또한 정규 표현식을 활용한 고급 검색·치환은 `re` 모듈에서 제공합니다.