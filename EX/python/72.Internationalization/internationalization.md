# 제72장 – 국제화와 현지화

전 세계 사용자를 위한 애플리케이션을 만들려면 텍스트를 번역하고 날짜, 시간, 숫자 형식과 같은 문화적 규약을 적용해야 합니다. 파이썬에는 이런 작업을 지원하는 여러 모듈이 있습니다: `gettext`는 메시지 번역을, `locale`은 문화권에 맞는 포맷과 정렬을, `calendar`는 현지화된 월·요일 이름을 제공합니다. 날짜와 시간을 처리할 때는 순진(`naive`)한 `datetime`과 시간대 정보를 포함한 `aware` 객체의 차이를 기억하고, `tzinfo` 속성이 시간대 정보를 어떻게 인코딩하는지 이해해야 합니다【694448817925088†L105-L133】.

## `gettext`로 메시지 번역

`gettext`는 GNU gettext 인터페이스를 구현합니다. `gettext.translation(domain, localedir, languages)`를 호출해 번역 카탈로그를 로드하고, 반환된 객체의 `gettext()` 메서드(또는 단축명 `_()`)를 호출해 문자열을 번역합니다. 코드에서 번역 가능한 문자열은 `_('메시지')`로 표시합니다. `xgettext` 명령줄 도구를 사용해 이러한 문자열을 `.pot` 파일로 추출하고 번역자들이 언어별 `.po` 파일을 만들도록 할 수 있습니다.

```python
import gettext

lang = gettext.translation('myapp', localedir='locale', languages=['es'])
lang.install()

print(_('Hello, world!'))  # 스페인어 번역이 있으면 "¡Hola, mundo!" 출력
```

## `locale`을 통한 문화권 포맷

`locale` 모듈은 숫자와 날짜 포맷, 정렬 및 통화 기호에 대한 POSIX 로케일 기능을 제공합니다. `locale.setlocale(locale.LC_ALL, '')`을 호출하여 사용자의 기본 로케일을 사용하거나 특정 로케일 코드를 지정할 수 있습니다. `locale.currency()`와 `locale.format_string()`과 같은 함수는 활성 로케일에 따라 출력 형식을 조정합니다.

## 캘린더 이름

`calendar` 모듈은 `month_name`과 `day_name` 시퀀스를 제공하여 로케일에 맞는 월과 요일 이름을 반환합니다. 예를 들어, 독일 로케일에서 3월을 출력하려면 다음과 같이 합니다:

```python
import locale
import calendar

locale.setlocale(locale.LC_TIME, 'de_DE.utf8')
print(calendar.month_name[3])  # 독일어 로케일에서는 'März'
```

## 요약

`gettext`를 사용해 메시지 문자열을 추출하고 번역하세요. `locale`을 사용해 숫자, 날짜, 통화 등을 문화권에 맞게 포맷하고, `calendar`와 결합해 월과 요일 이름을 현지화하세요. 여러 지역에 맞는 날짜와 시간을 표시할 때는 시간대 정보를 포함한 `datetime` 객체를 사용하는 것이 중요합니다【694448817925088†L105-L133】.