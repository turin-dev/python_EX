# 53장 – `decimal`과 `fractions`를 이용한 정확한 연산

이진 부동소수점 표현은 많은 단순한 십진수를 정확히 표현할 수 없다. 예를 들어 `0.1 + 0.1 + 0.1 - 0.3`을 계산하면 반올림 오차 때문에 아주 작은 비영값이 나온다. `decimal`과 `fractions` 모듈은 금융 및 과학 계산을 위한 정확한 십진수 연산과 유리수 연산을 제공한다【224278241315818†L68-L87】.

## Decimal 고정소수점 산술

`decimal` 모듈은 임의 정밀도의 십진 부동소수점을 구현한다. `Decimal` 객체는 유효 자릿수와 값을 정확하게 저장한다. `0.1 + 0.1 + 0.1 - 0.3`과 같은 연산도 Decimal을 사용하면 0.1이 정확하게 표현되므로 결과가 0이 된다【224278241315818†L68-L87】. 정밀도와 반올림 방식은 컨텍스트를 통해 제어할 수 있으며 기본 정밀도는 28자리다. 모듈은 `ROUND_HALF_EVEN`, `ROUND_DOWN` 등 다양한 반올림 모드를 지원한다【224278241315818†L90-L133】.

```python
from decimal import Decimal, getcontext

print(Decimal('0.1') + Decimal('0.1') + Decimal('0.1') - Decimal('0.3'))  # 0.0

# 정밀도 조정
getcontext().prec = 4
print(Decimal('1') / Decimal('3'))  # 0.3333
```

Decimal 연산은 `DivisionByZero`, `InvalidOperation`과 같은 시그널을 발생시킬 수 있으므로, 이러한 조건을 무시하거나 감지하도록 컨텍스트를 조정할 수 있다【224278241315818†L121-L133】.

## `fractions.Fraction`을 이용한 유리수 연산

`fractions` 모듈의 `Fraction` 클래스는 유리수를 정확하게 표현한다. 분자와 분모를 지정하여 만들 수 있으며, float나 Decimal, 문자열로부터도 생성할 수 있다. 예를 들어 `Fraction(2, 3)`은 2/3을 나타내고, `Fraction('3.75')`는 15/4가 된다. float는 정확하지 않기 때문에 그대로 변환하면 예상과 다른 결과가 나올 수 있다. 이진 반올림 문제를 피하려면 문자열 입력을 사용하는 것이 좋다【227678071871739†L51-L110】.

```python
from fractions import Fraction

print(Fraction(1, 3) + Fraction(2, 3))  # 1
print(Fraction('0.1') + Fraction('0.2'))  # 3/10

# float 변환 – 이진 표현에 주의한다
print(Fraction(1.1))  # 2476979795053773/2251799813685248
```

Fraction 객체는 사칙연산, float와 Decimal로의 변환, 분자와 분모를 최대공약수로 나눠 간단히 하는 정규화 기능을 지원한다.

## 요약

애플리케이션에서 정확한 십진수 값(예: 재무 계산)이 필요하다면 `decimal.Decimal`을 사용하고 적절한 정밀도와 반올림 모드를 설정하라【224278241315818†L90-L133】. 유리수 연산이 필요할 때는 `fractions.Fraction`을 사용하여 숫자를 정수의 비율로 정확하게 표현하고 이진 반올림 문제를 피할 수 있다【227678071871739†L51-L110】.