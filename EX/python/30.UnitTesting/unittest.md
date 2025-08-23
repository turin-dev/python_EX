# 30. 단위 테스트: `unittest` 모듈

`unittest` 모듈은 파이썬 표준 라이브러리에 포함된 **xUnit 스타일의 테스트 프레임워크**다. 문서에서는 테스트 자동화, 반복 실행, 집합화, 독립적인 테스트 실행, 결과 수집 도구를 제공한다고 설명한다【831634433666892†L72-L107】. 테스트 케이스는 `unittest.TestCase`를 상속하는 클래스로 정의한다.

## 기본 구조

테스트 클래스는 `setUp()`과 `tearDown()` 메서드를 통해 각 테스트 실행 전후에 필요한 준비와 정리를 수행한다. 실제 테스트는 `test_`로 시작하는 메서드에 정의하며, 다양한 `assert*` 메서드를 사용해 조건을 검증한다【831634433666892†L142-L170】.

```python
import unittest

def add(x, y):
    return x + y

class AddTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp called')

    def tearDown(self):
        print('tearDown called')

    def test_add_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-1, -2), -3)

if __name__ == '__main__':
    unittest.main()
```

## 테스트 스위트와 러너

`unittest`는 여러 테스트 케이스를 묶은 **테스트 스위트(TestSuite)**를 만들 수 있다. 스위트는 테스트 러너(TestRunner)에 의해 실행되고, 결과를 표준 출력이나 보고서 형태로 표시한다. 기본 러너로는 `unittest.TextTestRunner`가 제공된다.

```python
suite = unittest.TestSuite()
suite.addTest(AddTestCase('test_add_positive'))
suite.addTest(AddTestCase('test_add_negative'))
runner = unittest.TextTestRunner()
runner.run(suite)
```

## 주요 `assert*` 메서드

| 메서드 | 설명 |
|---|---|
| `assertEqual(a, b)` | `a == b`가 참인지 확인 |
| `assertTrue(expr)` | `expr`이 참인지 확인 |
| `assertFalse(expr)` | `expr`이 거짓인지 확인 |
| `assertRaises(exc, func, *args, **kwargs)` | 예외가 발생하는지 확인 |
| `assertAlmostEqual(a, b, places=7)` | 실수 `a`와 `b`가 소수점 이하 `places` 자리까지 거의 같은지 확인 |

단위 테스트를 작성하면 코드 변경 시 기능이 손상되지 않았는지 자동으로 확인할 수 있다. 지속적 통합(CI) 환경에서는 모든 커밋에 대해 테스트를 실행하도록 설정하여 품질을 보장한다.