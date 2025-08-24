# 제80장 – 데이터 포매팅과 보기 좋게 출력하기

파이썬은 데이터를 포맷하고 표시하는 다양한 방법을 제공합니다. `format()` 함수나 f‑문자열을 사용하여 문자열에 표현식을 삽입할 수 있으며, 파이썬 3.12에서는 f‑문자열의 오류 메시지와 디버깅 지원이 향상되었습니다【385620794081796†L109-L127】. `pprint` 모듈은 복잡한 데이터 구조를 보기 좋은 형태로 출력하고, `textwrap`은 텍스트를 고정된 폭으로 감쌀 수 있도록 도와줍니다.

## f‑문자열과 `format()` 함수

f‑문자열은 중괄호 안의 표현식을 평가하고 형식 지정자를 지원합니다(예: `:.2f`는 소수점 둘째 자리까지의 부동 소수점, `:05d`는 5자리로 0을 채운 정수). `str.format()` 메서드는 위치 인수나 이름 인수를 사용하여 비슷한 기능을 제공합니다.

```python
name = "Alice"
score = 93.4567
print(f"{name} scored {score:.2f} points")  # 'Alice scored 93.46 points'
print("{0} scored {1:.1f} points".format(name, score))
```

## `pprint`로 보기 좋게 출력하기

`pprint` 모듈의 `pprint()` 함수는 중첩된 데이터 구조를 들여쓰기와 키 정렬을 통해 읽기 쉽게 출력합니다. `pformat()`은 포맷된 문자열을 반환합니다. 복잡한 딕셔너리나 리스트를 디버깅할 때 유용합니다.

```python
from pprint import pprint

data = {
    "name": "Bob",
    "scores": [88, 92, 79],
    "details": {"age": 30, "city": "Seoul"},
}
pprint(data)
```

## `textwrap`으로 텍스트 감싸기

`textwrap`은 긴 문자열이나 단락을 지정한 폭으로 감쌉니다. `textwrap.fill()`은 텍스트를 한 줄 문자열로 감싸고, `textwrap.dedent()`는 공통 들여쓰기를 제거합니다.

```python
import textwrap

paragraph = (
    "Python is an amazing language that offers many features including easy readability, "
    "a vast standard library, and cross‑platform support."
)
print(textwrap.fill(paragraph, width=40))
```

## 요약

f‑문자열과 `str.format()`을 사용하여 유연한 문자열 포매팅을 구현하세요. `pprint`는 복잡한 구조를 보기 좋게 출력하고, `textwrap`은 긴 텍스트를 지정한 폭으로 감싸는 데 유용합니다. 파이썬 3.12는 f‑문자열의 오류 메시지와 디버그 지원을 개선하였습니다【385620794081796†L109-L127】.