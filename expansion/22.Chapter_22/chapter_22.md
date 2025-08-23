# 22장 – 로깅과 디버깅 기법

복잡한 봇을 개발하다 보면 예상치 못한 문제를 빠르게 파악하기 위해 로그를 남기는 것이 중요합니다. `discord.py`는 Python의 표준 로깅 시스템을 사용하며, 적절한 로깅 설정을 통해 메시지 내용, 발생 시간, 심각도 등을 손쉽게 확인할 수 있습니다. 또한 `discord.utils.setup_logging()` 도우미 함수는 라이브러리 내부 로거에 대한 기본 구성을 제공하여 HTTP 요청과 이벤트에 관한 유용한 정보를 출력합니다【840359539202996†L78-L133】.

## 기본 로깅 설정

파이썬 로깅을 활성화하려면 모듈을 임포트하고 루트 로거를 설정합니다. 콘솔과 파일 모두에 로그를 남기는 간단한 예시는 다음과 같습니다.

```python
import logging
import discord

# 로그 레벨과 포맷 지정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)

# discord.py 내부 로거 설정
discord.utils.setup_logging()
```

이 설정은 콘솔과 `bot.log` 파일에 `INFO` 이상 레벨의 메시지를 기록합니다. 라이브러리 내부에서 발생하는 디버그 메시지를 보고 싶다면 `level`을 `logging.DEBUG`로 조정합니다.

## 커스텀 로거와 필터링

봇에서 특정 모듈이나 기능에 대한 로그만 별도로 관리하려면 커스텀 로거를 생성할 수 있습니다. 예를 들어 데이터베이스 모듈의 로그를 별도 파일에 저장하려면 다음처럼 할 수 있습니다.

```python
db_logger = logging.getLogger("bot.database")
db_logger.setLevel(logging.INFO)
db_handler = logging.FileHandler("db.log", encoding="utf-8")
db_logger.addHandler(db_handler)

db_logger.info("연결 성공")
db_logger.warning("쿼리 성능이 느립니다")
```

로그 메시지의 양을 줄이고 싶다면 특정 레벨 이상만 기록하는 필터를 추가하거나, `discord.Client`의 `max_messages` 설정으로 캐시 크기를 조절하여 메모리 사용량을 줄일 수 있습니다【549557713116431†L69-L76】.

## 디버거 사용

런타임 동안 코드를 단계별로 실행하고 상태를 확인하려면 파이썬 표준 디버거 `pdb`를 활용할 수 있습니다. 코드 중간에 `import pdb; pdb.set_trace()`를 삽입하면 실행이 해당 줄에서 멈추고, 변수 값과 스택 프레임을 살펴볼 수 있는 대화형 프롬프트가 나타납니다【637898121780976†L56-L90】. 또한 파이썬 3.7 이상에서는 간단히 `breakpoint()` 함수를 호출하여 동일한 효과를 낼 수 있습니다. 디스코드 봇처럼 비동기 코드에서도 디버거를 사용할 수 있지만, 이벤트 루프를 차단하지 않도록 주의해야 합니다.

## 요약

효과적인 로깅은 문제를 빠르게 찾아내고 서비스 상태를 파악하는 데 큰 도움이 됩니다. 표준 로깅 설정을 통해 콘솔과 파일에 구조화된 정보를 남기고, 필요하다면 커스텀 로거를 만들어 특정 기능을 분리하세요. 또한 디버거를 활용해 복잡한 비동기 흐름을 직접 따라가며 원인을 분석하는 방법을 익히면, 디스코드 봇 개발의 생산성이 크게 높아집니다.


