# 35장 – 테스트와 디버깅

안정적인 봇을 만들기 위해서는 기능을 자동화된 테스트로 검증하고, 문제를 분석할 수 있는 디버깅 도구를 활용해야 합니다. 파이썬 표준 라이브러리의 `unittest`는 테스트 케이스, 테스트 스위트, 테스트 러너를 제공하며【831634433666892†L72-L107】, 봇의 함수와 명령을 테스트하는 데 사용할 수 있습니다. 또한 `pytest`나 `discord.ext.test`와 같은 서드파티 라이브러리도 비동기 함수를 지원합니다.

## 단위 테스트 작성하기

테스트 클래스는 `unittest.TestCase`를 상속하고, `setUp()`과 `tearDown()` 메서드에서 테스트 환경을 준비합니다. 아래 예제는 두 수를 더하는 간단한 함수를 테스트하는 방법을 보여 줍니다.

```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertNotEqual(add(2, 2), 5)

if __name__ == '__main__':
    unittest.main()
```

비동기 함수나 봇 명령을 테스트하려면 `asyncio.run()`을 사용하거나, `pytest`의 `pytest.mark.asyncio` 데코레이터를 사용할 수 있습니다.

## 봇 명령 테스트

`discord.ext.test` 라이브러리는 테스트 환경에서 가짜 컨텍스트와 메시지를 생성하여 봇 명령을 실행하고 반환 값을 검증할 수 있게 해 줍니다. 예를 들어 `!ping` 명령이 `pong`을 반환하는지 테스트하려면 다음과 같이 합니다.

```python
import pytest
from discord.ext import test as dpytest

@pytest.mark.asyncio
async def test_ping(bot):
    dpytest.configure(bot)
    await dpytest.message("!ping")
    assert dpytest.get_message().content == "pong"
```

테스트에서 봇 객체를 초기화할 때는 실제 Discord API를 호출하지 않도록 `loop=None` 등의 설정을 활용하고, 데이터베이스나 HTTP 요청을 목(mock) 처리해야 합니다.

## 디버깅 기법

코드가 예상대로 동작하지 않을 때는 Python의 `pdb` 모듈로 중단점(breakpoint)을 설정하여 변수 값을 확인하고 함수 호출 흐름을 추적할 수 있습니다【637898121780976†L56-L90】. 또한 `logging`을 통해 디버그 메시지를 출력하면 테스트나 실제 실행 환경에서도 상태를 확인할 수 있습니다【840359539202996†L78-L133】.

## 요약

테스트는 코드 품질을 높이고 리팩터링 시 회 regressions을 방지합니다. `unittest`를 사용해 기본 테스트 구조를 만들고, 필요한 경우 비동기 테스트 라이브러리를 활용하세요. 디버깅 도구와 로깅을 적극적으로 사용하여 문제를 빠르게 발견하고 해결하는 습관을 들이면 봇 개발이 훨씬 수월해집니다.

