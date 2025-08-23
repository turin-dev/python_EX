# 46장 – 로깅과 메트릭

봇을 운영하다 보면 다양한 이벤트와 오류를 추적해야 합니다. Python의 `logging` 모듈은
유연한 로깅 시스템을 제공하며, `discord.py`도 내부적으로 이를 사용합니다. 또한 봇의
동작을 모니터링하고 카운트하는 메트릭 시스템을 구축하면 문제를 빠르게 진단하는 데
도움이 됩니다.

## 로깅 설정하기

`logging` 모듈을 사용하면 여러 로거를 계층적으로 구성할 수 있습니다. 문서에서는
루트 로거와 하위 로거를 통해 메시지를 처리하는 방법과 `basicConfig`를 사용해 기본
설정을 할 수 있다고 설명합니다【840359539202996†L78-L133】. 주요 포인트는 다음과 같습니다:

* **로거 이름을 모듈 경로로 지정**: 각 파일에서 `logger = logging.getLogger(__name__)`를 호출하면
  패키지 구조에 따라 상위 로거의 설정을 자동으로 상속합니다.
* **레벨 설정**: `logger.setLevel(logging.INFO)` 등으로 로그 레벨을 지정하면 그 이하 레벨의 메시지는 무시됩니다.
* **핸들러와 포매터**: `logging.FileHandler`나 `logging.StreamHandler`를 추가하여 로그를 파일과 콘솔에
  동시에 출력할 수 있습니다. 포매터를 사용해 날짜·레벨·메시지 형식을 통일합니다.
* **discord.py 내부 로그 활성화**: 라이브러리의 동작을 확인하려면 `logging.getLogger("discord")`의 레벨을
  `INFO` 이상으로 설정하면 됩니다.

다음 예제는 파일과 콘솔에 로그를 기록하며, `discord` 로거의 레벨을 조정합니다.

```python
import logging

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 콘솔 핸들러
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 파일 핸들러
    file_handler = logging.FileHandler("bot.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # discord 로거 설정
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.WARNING)

setup_logging()
```

위 함수는 루트 로거를 구성하고, 콘솔과 파일에 동일한 포맷으로 로그를 남깁니다. `discord` 로거의
레벨을 `WARNING`으로 설정하면 미세한 디버그 메시지는 무시하고 중요도 높은 메시지만 기록합니다.

## 메트릭 수집

메트릭은 봇의 동작을 관찰하고 문제를 사전에 발견하는 데 도움이 됩니다. 간단한 방법으로는
딕셔너리를 사용해 명령 사용 횟수를 집계할 수 있습니다. 더 복잡한 시스템에서는
`prometheus_client`나 `statsd` 라이브러리를 사용해 모니터링 대시보드와 연동할 수 있습니다.

아래 예제는 명령 실행 횟수를 기록하고, 10회마다 로그를 출력하는 간단한 메트릭 시스템입니다.

```python
from collections import Counter
from discord.ext import commands

command_counts = Counter()

class MetricsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        command_counts[ctx.command.qualified_name] += 1
        total = command_counts[ctx.command.qualified_name]
        if total % 10 == 0:
            ctx.bot.logger.info(f"명령 '{ctx.command}'가 총 {total}회 호출되었습니다.")


async def setup(bot: commands.Bot):
    bot.add_cog(MetricsCog(bot))
```

이 코그는 `on_command_completion` 이벤트를 통해 명령 실행이 완료될 때마다 카운터를 증가시킵니다. 10회
단위로 메시지 로거에 기록하여 사용량을 모니터링할 수 있습니다. 실제 운영 환경에서는 수집된 데이터를
외부 모니터링 시스템으로 전송하여 그래프를 그리거나 알림을 설정할 수 있습니다.

## 요약

`logging` 모듈을 적절히 구성하면 봇의 동작과 오류를 체계적으로 기록할 수 있습니다. 루트 로거와
서브 로거의 레벨을 설정하고, 콘솔과 파일 핸들러를 추가해 로그를 다양한 방식으로 저장하세요【840359539202996†L78-L133】.
또한 간단한 메트릭 수집을 통해 명령 사용량을 파악하고, 필요에 따라 외부 모니터링 도구와 연계하여
서비스의 상태를 상시 확인할 수 있습니다.