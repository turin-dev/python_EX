# 제74장 – 고급 로깅 설정

파이썬의 `logging` 모듈은 매우 유연하게 구성할 수 있습니다. 기본적인 사용에서는 `logging.basicConfig()`로 로그 수준과 포맷을 설정하지만, 대규모 애플리케이션에서는 여러 핸들러, 필터, 포매터가 필요할 수 있습니다. 문서에 따르면 로거는 계층 구조를 가지며, 호출은 상위 로거로 전파되지만 비활성화할 수도 있습니다【840359539202996†L78-L133】. 로깅은 코드 내에서 직접 구성할 수도 있고 `logging.config`를 통해 설정 파일로 구성할 수도 있습니다.

## 핸들러와 포매터

핸들러는 로그 레코드를 다양한 대상으로 전송합니다. 각 핸들러는 자체 로그 수준과 포매터를 가질 수 있습니다. 예를 들어 `StreamHandler`는 표준 에러에 기록하고, `FileHandler`는 디스크 파일에, `SMTPHandler`는 이메일로 로그를 보냅니다.

```python
import logging

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

file = logging.FileHandler("app.log")
file.setLevel(logging.DEBUG)
file.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s"))

logger.addHandler(console)
logger.addHandler(file)

logger.debug("This goes to the file only")
logger.info("This goes to both console and file")
```

## 구성 파일

`logging.config` 모듈은 딕셔너리, JSON 또는 INI 스타일 파일에서 설정을 읽어 들입니다. `dictConfig()`나 `fileConfig()`를 사용하여 한번에 구성할 수 있습니다. 설정에서는 로거, 핸들러, 포매터와 그 관계를 정의합니다.

```python
import logging.config

config = {
    'version': 1,
    'formatters': {
        'simple': {'format': '%(levelname)s:%(name)s:%(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO',
        },
    },
    'loggers': {
        '': {'handlers': ['console'], 'level': 'DEBUG'},
    },
}
logging.config.dictConfig(config)
logging.getLogger(__name__).info("Hello from dictConfig")
```

## 필터

필터는 로그 레코드를 핸들러에 전달할지 여부를 결정합니다. `logging.Filter`를 서브클래싱하거나 핸들러의 `filter()`에 함수를 전달해 특정 모듈에서 오는 메시지를 제외하거나 특정 수준만 허용하는 등의 동작을 구현할 수 있습니다.

## 요약

고급 로깅 구성은 로그 출력을 여러 목적지와 형식으로 전달할 수 있게 해 줍니다. 핸들러, 포매터, 필터를 사용하여 메시지가 어디에서 어떻게 표시될지 제어하세요. 로거는 기본적으로 상위 로거로 전파되므로 적절히 수준을 설정해야 합니다【840359539202996†L78-L133】.