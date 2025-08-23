# 21. 데코레이터와 함수 래퍼

파이썬에서 **데코레이터(decorator)**는 함수를 다른 함수에 전달하거나 반환하여 기존 함수의 동작을 수정하는 고급 기능이다. 파이썬 문서의 용어집은 데코레이터를 *“함수를 반환하는 함수로서, `@wrapper` 표기법은 `f = wrapper(f)`와 같은 의미다”*라고 설명한다【212515192382289†L370-L395】. 데코레이터는 반복되는 전처리·후처리 로직을 쉽게 재사용하게 해 준다.

## 기본 형태

- 데코레이터는 다른 함수를 인자로 받아 내부에서 호출 후 반환값을 가공하거나 부수 효과를 더한다.
- `@decorator` 표기법을 사용하면 함수 정의 바로 위에 붙일 수 있고, 이는 `func = decorator(func)`와 같다【212515192382289†L370-L395】.
- 데코레이터 함수 내부에서 원본 함수의 메타데이터를 유지하려면 `functools.wraps`를 사용한다.

다음은 간단한 로깅 데코레이터의 예시이다.

```python
import functools

def log_call(func):
    """호출 시 함수 이름과 인자를 로그로 출력하는 데코레이터."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

add(3, 5)  # 데코레이터가 호출 과정을 로그로 출력
```

## 여러 데코레이터 쌓기

여러 데코레이터를 하나의 함수에 적용할 수 있다. 적용 순서는 가장 위에 있는 데코레이터부터 아래로 내려가며 함수가 감싸지는 순서다. 예를 들어:

```python
@decorator_a
@decorator_b
def my_func():
    pass
```

위 코드는 `my_func = decorator_a(decorator_b(my_func))`와 같다. 여러 데코레이터를 조합하면 인증, 로깅, 캐싱 등 다양한 기능을 함수에 부가할 수 있다.

## 매개변수를 받는 데코레이터

데코레이터도 함수를 반환하는 함수이기 때문에 인자를 받을 수 있다. 일반적으로 한 번 더 중첩된 함수를 사용한다.

```python
def repeat(n):
    """함수를 n번 반복 호출하는 데코레이터."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Python")
```

## 데코레이터의 활용 예

- **권한 검사**: 인증된 사용자만 특정 함수를 실행하도록 제한할 수 있다.
- **메모이제이션**: `functools.cache` 또는 `lru_cache`를 통해 함수 결과를 캐싱하여 성능을 높인다【974880726755322†L56-L69】.
- **타이밍 측정**: 함수 실행 시간을 측정하거나 로깅하는 데코레이터를 작성할 수 있다.
- **형 검사**: 함수 인자나 반환값의 타입을 체크하여 예외를 발생시키는 데코레이터를 만들 수 있다.

잘 설계된 데코레이터는 코드 중복을 줄이고 가독성을 높여 준다.