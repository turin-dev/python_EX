# 모니터링과 메트릭

봇의 안정성을 높이기 위해서는 로깅과 모니터링을 통해 문제를 조기에 발견하고, 주요 지표를 수집해 성능을 분석하는 것이 중요합니다. 이 장에서는 Python의 `logging` 모듈을 활용해 다양한 로그를 기록하는 방법과, 명령 호출 횟수 등 간단한 메트릭을 수집하는 기법을 소개합니다.

## 로깅 설정 고급

`logging` 모듈은 기본적으로 콘솔에 로그를 출력하지만, 로테이팅 파일 핸들러나 이메일/HTTP 핸들러 등 다양한 출력 방식을 지원합니다. 또한 `logging.config.dictConfig`를 사용하면 설정을 코드가 아닌 딕셔너리로 정의할 수 있어 관리가 쉽습니다. 아래 예제는 콘솔과 파일에 서로 다른 로그 레벨과 포맷으로 로그를 남기는 설정입니다【840359539202996†L78-L133】.

```python
import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "bot.log",
            "maxBytes": 1024*1024,
            "backupCount": 3,
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

logger.info("로깅 시스템이 설정되었습니다")
```

이 설정에서는 INFO 레벨 로그는 콘솔과 파일 모두에 출력되고, DEBUG 레벨 로그는 파일에만 기록됩니다. 로그 파일은 1MB가 넘으면 자동으로 새로운 파일로 교체되며 최대 3개까지 유지됩니다.

## 간단한 메트릭 수집

외부 모니터링 도구를 사용하지 않는 경우에도, 봇 내부에서 중요한 지표를 수집할 수 있습니다. 가장 간단한 방법은 명령 호출 횟수, 에러 발생 횟수 등의 카운터를 딕셔너리나 `collections.Counter`로 저장하는 것입니다. 아래는 특정 명령 호출 횟수를 기록하고, `/stats` 명령으로 통계를 출력하는 예제입니다.

```python
from discord.ext import commands
from collections import Counter

class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.command_calls = Counter()

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        self.command_calls[ctx.command.qualified_name] += 1

    @commands.hybrid_command(name="stats", description="명령 사용 통계 출력")
    async def stats(self, ctx: commands.Context):
        lines = [f"{name}: {count}" for name, count in self.command_calls.items()]
        report = "\n".join(lines) if lines else "통계가 없습니다."
        await ctx.send(f"명령 사용 통계:\n{report}")
```

보다 복잡한 메트릭(메모리 사용량, 응답 시간 등)을 수집하려면 `prometheus_client`와 같은 라이브러리를 도입해 HTTP 엔드포인트를 통해 외부 모니터링 시스템과 연동할 수 있습니다. 또한 장애를 빠르게 탐지하기 위해 로깅과 메트릭을 통합 서비스(예: Sentry, Grafana)로 전송하는 것이 좋습니다.

## 정리

체계적인 로깅과 지표 수집은 봇의 상태를 파악하고 문제를 신속히 해결하는 데 큰 도움이 됩니다. 설정을 모듈화하고 외부 서비스와 연동해 대시보드를 구축하면, 운영 중 발생하는 이슈를 시각적으로 확인할 수 있습니다.

