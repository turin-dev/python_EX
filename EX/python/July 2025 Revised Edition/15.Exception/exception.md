---

# 예외 처리

## 예외란?

- 프로그램 실행 중 예상치 못한 상황에서 발생하는 오류를 말합니다.
- 예외가 발생하면 기본적으로 프로그램이 중단되므로, 적절한 예외 처리가 필요합니다.

## try / except 구문

- 예외가 발생할 가능성이 있는 코드를 `try` 블록에 작성하고, 발생한 예외를 `except` 블록에서 처리합니다.

```python
try:
    x = int("not a number")
except ValueError as e:
    print("변환 오류:", e)
```

## 다중 except, else, finally

- 여러 종류의 예외를 각각 처리하기 위해 `except` 구문을 여러 번 사용할 수 있습니다.
- `else` 블록은 예외가 발생하지 않았을 때 실행되고, `finally` 블록은 예외 발생 여부와 상관없이 항상 실행됩니다.

```python
try:
    f = open("data.txt")
    data = f.read()
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
else:
    print("파일 읽기 완료")
finally:
    f.close()
```

## 예외 발생시키기

- `raise` 키워드를 사용하여 특정 조건에서 예외를 명시적으로 발생시킬 수 있습니다.

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return a / b

try:
    result = divide(10, 0)
except ZeroDivisionError as e:
    print(e)
```

## 요약

예외 처리 구문을 사용하면 프로그램의 안정성을 높이고, 예외 상황에서도 적절한 메시지를 제공하며, 필요한 정리 작업을 수행할 수 있습니다. `try`/`except`/`else`/`finally` 구문을 적절히 사용하여 코드의 예외를 관리하십시오.

## 추가 설명

### 내장 예외와 예외 계층

파이썬에는 `ZeroDivisionError`, `ValueError`, `TypeError` 등 수십 개의 내장 예외가 있으며, 모두 `BaseException` 클래스를 상속합니다. `Exception`은 대부분의 사용자 코드에서 처리하는 기본 클래스입니다. 가능한 한 구체적인 예외를 처리하고, 최상위에서는 `Exception`을 포괄적으로 잡아 로깅하거나 재전파할 수 있습니다.

### 예외 연결과 `raise from`

새로운 예외를 발생시킬 때 원래 예외 정보를 유지하기 위해 `raise NewError() from original_error` 구문을 사용할 수 있습니다. 이렇게 하면 예외 체인(chain)이 생성되어 디버깅에 도움이 됩니다.

```python
try:
    int('not a number')
except ValueError as e:
    raise RuntimeError('변환 실패') from e
```

### assert 문

`assert`는 조건이 거짓일 때 `AssertionError`를 발생시켜 디버깅을 돕는 도구입니다. 프로덕션 환경에서는 최적화 모드(`python -O`)로 실행하면 assert 문이 제거될 수 있습니다.

```python
def sqrt(x):
    assert x >= 0, '음수는 제곱근을 계산할 수 없습니다.'
    return x ** 0.5
```

### 사용자 정의 예외

특정 도메인에 대한 의미 있는 오류를 제공하려면 예외 클래스를 직접 정의할 수 있습니다. 사용자 정의 예외는 일반적으로 `Exception`을 상속받습니다.

```python
class ValidationError(Exception):
    pass

def validate_age(age):
    if age < 0:
        raise ValidationError('나이는 0 이상이어야 합니다.')

try:
    validate_age(-5)
except ValidationError as e:
    print('입력 오류:', e)
```

### warnings 모듈

`warnings` 모듈을 사용하면 예외를 발생시키는 대신 경고를 출력할 수 있습니다. 이는 앞으로 사라질 기능을 알리거나, 성능 문제가 있을 때 사용자에게 알려줄 때 유용합니다.