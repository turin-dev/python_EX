# 예외 처리 예제

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return a / b

# try / except 예제
try:
    x = int("not a number")
except ValueError as e:
    print('변환 오류:', e)

# 다중 except, else, finally 예제
try:
    f = open('data.txt')
    data = f.read()
except FileNotFoundError:
    print('파일을 찾을 수 없습니다.')
else:
    print('파일 읽기 완료')
finally:
    f.close()

# 예외 발생시키기 사용 예
try:
    result = divide(10, 0)
except ZeroDivisionError as e:
    print(e)

# raise from 사용 예제
try:
    int('abc')
except ValueError as e:
    try:
        raise RuntimeError('변환 실패') from e
    except RuntimeError as re:
        print('chained exception:', re, 'cause:', re.__cause__)

# assert 문 예제
def sqrt(x):
    assert x >= 0, '음수는 제곱근을 계산할 수 없습니다.'
    return x ** 0.5
try:
    sqrt(-1)
except AssertionError as e:
    print('assertion error:', e)

# 사용자 정의 예외 클래스
class ValidationError(Exception):
    pass

def validate_age(age):
    if age < 0:
        raise ValidationError('나이는 0 이상이어야 합니다.')

try:
    validate_age(-5)
except ValidationError as e:
    print('validation error:', e)

# warnings 모듈 사용 예제
import warnings
warnings.warn('이 기능은 곧 사라질 예정입니다.', DeprecationWarning)