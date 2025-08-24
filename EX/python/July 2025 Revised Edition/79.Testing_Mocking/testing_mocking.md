# 제79장 – 테스트와 모킹

자동화된 테스트는 코드가 예상대로 동작하는지 확인하고 회귀를 방지합니다. 파이썬의 `unittest` 프레임워크는 테스트 케이스를 작성하고 이를 모아 실행할 수 있는 클래스를 제공합니다【831634433666892†L72-L107】. `unittest.mock` 모듈은 테스트 중에 시스템의 일부를 모의 객체로 교체하고 이 객체들이 어떻게 사용되는지 주장(assert)할 수 있도록 해 줍니다.

## `unittest`로 테스트 작성하기

`unittest.TestCase`를 상속한 클래스를 만들고 `test_` 접두어로 시작하는 메서드를 정의하세요. `assertEqual()`, `assertTrue()`, `assertRaises()` 등과 같은 단언 메서드를 사용하여 예상 결과를 확인합니다. 프레임워크는 각 테스트에 대한 설정과 해제를 수행하는 메서드도 제공합니다【831634433666892†L72-L107】. 테스트를 실행하려면 테스트 스크립트에서 `unittest.main()`을 호출합니다.

```python
import unittest

def multiply(a, b):
    return a * b

class MultiplyTest(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(multiply(2, 3), 6)
    def test_zero(self):
        self.assertEqual(multiply(0, 5), 0)

if __name__ == "__main__":
    unittest.main()
```

`subTest()`를 사용하면 하나의 테스트 메서드 안에서 여러 관련 단언을 그룹화하여 첫 번째 실패에서 멈추지 않고 모든 입력을 검증할 수 있습니다.

## `unittest.mock`으로 모킹

`unittest.mock` 모듈은 `Mock`, `MagicMock`, `patch()`와 같은 클래스를 제공하여 테스트 중에 객체를 교체합니다. `patch()`를 데코레이터나 컨텍스트 매니저로 사용하면 테스트가 끝난 후 자동으로 원래 상태로 복원됩니다. 모의 객체에 대한 호출을 주장하거나 호출 인자를 검사할 수 있습니다.

```python
from unittest.mock import patch
import urllib.request

def fetch_url(url):
    with urllib.request.urlopen(url) as f:
        return f.read().decode()

@patch('urllib.request.urlopen')
def test_fetch_url(mock_urlopen):
    mock_response = mock_urlopen.return_value.__enter__.return_value
    mock_response.read.return_value = b"OK"
    assert fetch_url("http://example.com") == "OK"
    mock_urlopen.assert_called_once()

if __name__ == "__main__":
    test_fetch_url()
```

## 요약

`unittest`를 사용해 테스트 케이스를 구성하고, 단언 메서드와 설정/해제 훅으로 테스트를 체계화하세요【831634433666892†L72-L107】. `unittest.mock`을 사용하면 외부 의존성을 모의 객체로 대체하고 그 사용을 주장할 수 있습니다. 테스트는 코드의 정확성에 대한 확신을 높이고 리팩토링을 간편하게 만듭니다.