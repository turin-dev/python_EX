"""예제 28: datetime 모듈을 이용한 날짜와 시간 처리.

이 스크립트는 naive와 aware datetime 객체의 차이, 시간대 변환, 포맷팅과 파싱,
timedelta 계산을 보여 준다.
"""

from datetime import datetime, date, time, timedelta, timezone


def show_basics() -> None:
    d = date(2025, 8, 22)
    t = time(14, 30, 0)
    dt = datetime(2025, 8, 22, 14, 30)
    print('Date:', d)
    print('Time:', t)
    print('Datetime:', dt)
    print('now():', datetime.now())
    print('utcnow():', datetime.utcnow())


def timezone_conversion() -> None:
    utc = timezone.utc
    kst = timezone(timedelta(hours=9))
    now_utc = datetime.now(utc)
    now_kst = now_utc.astimezone(kst)
    print('UTC time:', now_utc)
    print('KST time:', now_kst)


def format_parse() -> None:
    fmt = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    text = now.strftime(fmt)
    parsed = datetime.strptime(text, fmt)
    print('Formatted:', text)
    print('Parsed:', parsed)


def timedelta_demo() -> None:
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    delta = tomorrow - today
    print('Seconds between today and tomorrow:', delta.total_seconds())


if __name__ == '__main__':
    show_basics()
    print('--- Timezone conversion ---')
    timezone_conversion()
    print('--- Format and parse ---')
    format_parse()
    print('--- Timedelta ---')
    timedelta_demo()