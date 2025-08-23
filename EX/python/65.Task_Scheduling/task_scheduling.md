# 제65장 – 작업 스케줄링과 타이머

프로그램에서 특정 시간이나 주기로 함수를 실행해야 하는 경우가 있습니다. 파이썬 표준 라이브러리는 실행을 지연하고 이벤트를 예약할 수 있는 여러 모듈을 제공합니다. `time` 모듈은 현재 스레드를 지정된 초 동안 일시 중지하는 `sleep()` 함수를 제공하고, `sched` 모듈은 미래 시점에 함수를 실행하는 간단한 이벤트 스케줄러를 구현합니다. 날짜와 시간을 기준으로 작업을 스케줄링할 때는 순진(`naive`)한 `datetime`과 시간대 정보를 포함한 `aware` 객체의 차이를 이해해야 합니다. `datetime` 문서는 `tzinfo` 속성을 사용해 시간대 정보를 인코딩하는 방법을 설명합니다【694448817925088†L105-L133】.

## 수면과 타이밍

`time.sleep(seconds)`는 현재 스레드를 주어진 초 동안 일시 정지합니다. 소수점 값을 전달하면 부분 초 지연을 지정할 수 있습니다. 경과 시간을 측정하려면 높은 해상도의 타이머인 `time.perf_counter()` 또는 `time.monotonic()`을 사용하세요.

```python
import time

start = time.perf_counter()
time.sleep(0.5)
elapsed = time.perf_counter() - start
print(f"Slept for {elapsed:.3f} seconds")
```

## `sched`를 이용한 간단한 스케줄링

`sched` 모듈은 스케줄러 클래스를 정의하며 예약된 이벤트를 관리합니다. 이벤트는 시간이 지난 순서대로 실행되며, 핸들러 실행이 끝날 때 새 이벤트를 예약하면 반복 이벤트를 만들 수 있습니다.

```python
import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name):
    print(f"Event: {name} at", time.strftime("%X"))

# 2초와 4초 뒤에 이벤트를 예약합니다
scheduler.enter(2, 1, print_event, argument=("first",))
scheduler.enter(4, 1, print_event, argument=("second",))

print("Starting scheduler at", time.strftime("%X"))
scheduler.run()
```

## 요약

`time.sleep()`을 사용하면 실행을 일시 중지하고, 고해상도 타이머를 통해 경과 시간을 측정할 수 있습니다. `sched` 모듈은 미래에 태스크를 실행할 수 있는 간단한 이벤트 스케줄러를 제공합니다. 날짜와 시간에 기반한 작업을 스케줄링할 때는 올바른 시간대가 지정된 `datetime` 객체를 사용해야 합니다【694448817925088†L105-L133】.