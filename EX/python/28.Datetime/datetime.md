# 28. 날짜와 시간: `datetime` 모듈

파이썬의 `datetime` 모듈은 날짜와 시간 처리에 필요한 클래스를 제공한다. 문서에서는 **“나이브(naive) 객체는 시간대(tzinfo)를 포함하지 않고, 어웨어(aware) 객체는 `tzinfo` 속성을 통해 시간대 정보를 보유한다”**고 설명한다【694448817925088†L105-L133】. 어웨어 객체는 서로 다른 시간대 간 변환을 가능하게 하지만, 나이브 객체는 단순 시간 연산에 적합하다.

## 날짜와 시간 생성

- `datetime.date(year, month, day)`는 날짜(연‑월‑일)를 나타낸다.
- `datetime.time(hour, minute, second)`는 시각(시‑분‑초)을 나타낸다.
- `datetime.datetime(year, month, day, hour, minute, second)`는 날짜와 시간을 모두 포함한다. `datetime.now()`는 시스템 로컬 시간을 반환하고, `datetime.utcnow()`는 UTC 기준 시간을 반환한다.

```python
from datetime import date, time, datetime

d = date(2025, 8, 22)
t = time(14, 30)
dt = datetime(2025, 8, 22, 14, 30)

print(d, t, dt)
print(datetime.now())  # 현재 로컬 시간
print(datetime.utcnow())  # UTC 시간
```

## 시간대 처리

`datetime.timezone` 클래스를 사용하면 고정 오프셋 시간대를 지정할 수 있다【694448817925088†L105-L133】. 또한 `pytz`나 `zoneinfo` 모듈(3.9+)을 사용하면 IANA 데이터베이스 기반의 실제 시간대를 적용할 수 있다.

```python
from datetime import datetime, timedelta, timezone

utc = timezone.utc
kst = timezone(timedelta(hours=9))  # 한국 표준시

now_utc = datetime.now(utc)
now_kst = now_utc.astimezone(kst)
print("UTC:", now_utc)
print("KST:", now_kst)
```

`astimezone()` 메서드는 어웨어 datetime 객체의 시간대를 변환한다. 시간대 없는 나이브 객체에 `tzinfo`를 설정하려면 `replace(tzinfo=...)`를 사용할 수 있다. 시간대와 관련된 연산을 올바르게 처리하려면 항상 어웨어 객체를 사용해야 한다.

## 날짜/시간 형식화 및 파싱

`strftime()` 메서드는 datetime 객체를 문자열로 포맷하고, `strptime()` 메서드는 문자열을 datetime으로 변환한다. 형식 지정 코드는 C의 `strftime`과 호환된다.

```python
fmt = "%Y-%m-%d %H:%M:%S"
now = datetime.now()
text = now.strftime(fmt)
parsed = datetime.strptime(text, fmt)
print(text, parsed)
```

## 시간 간격 연산

`datetime.timedelta` 객체는 두 날짜/시간 사이의 간격을 나타낸다. 덧셈과 뺄셈 연산을 통해 날짜 계산을 할 수 있다.

```python
from datetime import timedelta

today = datetime.now()
tomorrow = today + timedelta(days=1)
delta = tomorrow - today
print(delta.total_seconds(), "seconds")
```

날짜와 시간 처리는 복잡한 문제이므로, 시간대 정보와 표준을 준수하는 것이 중요하다.【694448817925088†L105-L133】