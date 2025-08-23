# 29. 로깅 시스템

`logging` 모듈은 파이썬 애플리케이션에서 메시지를 기록하기 위한 유연한 프레임워크를 제공한다. 문서는 **루트 로거의 설정에 따라 메시지가 어떻게 처리되는지 결정되며**, 모듈별로 다른 로거를 사용할 수 있다고 설명한다【840359539202996†L78-L133】. 로깅은 디버깅, 오류 추적, 운영 상태 모니터링 등에 필수적이다.

## 로거, 핸들러, 포매터

- **로거(Logger)**: 로그 메시지를 생성하는 객체. `logging.getLogger(name)`으로 생성하며 계층적 이름 공간을 가진다. 이름에 점(`.`)이 있으면 부모-자식 관계가 형성되어, 부모 로거의 설정을 상속한다【840359539202996†L78-L133】.
- **핸들러(Handler)**: 로그를 실제 목적지(콘솔, 파일, 네트워크 등)로 전달하는 객체.
- **포매터(Formatter)**: 로그 메시지의 포맷을 정의한다. 예를 들어 타임스탬프와 로그 레벨을 포함하도록 지정할 수 있다.

루트 로거는 `logging.basicConfig()` 호출로 간단히 설정할 수 있으며, 이후 `logging.getLogger(__name__)`을 호출하면 해당 모듈 이름을 가진 로거가 생성된다【840359539202996†L78-L133】.

## 기본 사용 예

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)

logger = logging.getLogger(__name__)

logger.debug('디버그 메시지')
logger.info('정보 메시지')
logger.warning('경고 메시지')
logger.error('오류 메시지')
logger.critical('치명적 오류')
```

## 핸들러와 포매터 커스터마이징

더 세밀한 제어가 필요하다면 로거에 직접 핸들러와 포매터를 추가할 수 있다. 예를 들어 파일 핸들러를 추가하고 오류 이상의 메시지만 기록하도록 설정할 수 있다.

```python
import logging

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

logger.addHandler(file_handler)

logger.info('콘솔에는 출력되지 않음 (루트 로거 미설정 시)')
logger.error('이 메시지는 파일에 기록됨')
```

## 로그 수준

로깅 메시지는 다음과 같은 심각도 수준을 가진다 (낮을수록 덜 심각).

| 수준 상수 | 의미 |
|---|---|
| `DEBUG` | 상세한 진단 정보 |
| `INFO` | 일반적인 실행 정보 |
| `WARNING` | 잠재적 문제 또는 주의 필요 |
| `ERROR` | 오류가 발생하여 기능이 실패함 |
| `CRITICAL` | 심각한 오류로 프로그램 실행 불가 |

적절한 로그 수준을 선택하면 필요하지 않은 메시지를 필터링하고 중요한 정보를 효과적으로 기록할 수 있다.