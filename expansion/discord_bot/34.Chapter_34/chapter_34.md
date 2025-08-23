# 34장 – 다국어 지원과 현지화(i18n)

글로벌 디스코드 서버에서 봇을 운영한다면 여러 언어로 명령과 메시지를 제공해야 합니다. Python 표준 라이브러리의 `gettext`와 `locale` 모듈은 문자열을 번역하고 지역화하는 데 유용하며, `discord.app_commands`는 슬래시 명령의 이름과 설명을 여러 언어로 정의하는 기능을 제공합니다.

## `gettext`로 문자열 번역하기

`gettext`는 .po/.mo 파일 형식의 번역 카탈로그를 사용해 문자열을 번역합니다. 기본 사용법은 다음과 같습니다.

```python
import gettext

# 번역 파일이 저장된 디렉터리 지정 및 언어 선택
ko = gettext.translation('messages', localedir='locales', languages=['ko'])
ko.install()
_ = ko.gettext  # '_' 별칭으로 사용

print(_('Hello'))  # 'Hello'에 대한 한국어 번역 출력
```

`locales/ko/LC_MESSAGES/messages.po` 파일을 작성하여 원문과 번역을 매핑하면, 코드에서 `_("Hello")`를 호출할 때 한국어 메시지가 반환됩니다. 번역되지 않은 경우 원문이 그대로 출력됩니다.

## 명령어 현지화

`discord.app_commands` 모듈은 슬래시 명령과 옵션의 이름과 설명에 대해 지역화된 문자열을 설정할 수 있는 `locale_str` 매개변수를 제공합니다. 다음 예제는 `en-US`와 `ko` 두 언어로 슬래시 명령을 정의하는 방법을 보여 줍니다.

```python
from discord import app_commands

@bot.tree.command(name="greet", description="Greets the user", name_localizations={"ko": "인사"}, description_localizations={"ko": "사용자에게 인사합니다"})
@app_commands.describe(name="Your name", name_localizations={"ko": "이름"})
async def greet(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello, {name}!")
```

사용자가 Discord 언어 설정을 한국어로 지정하면 `/인사` 명령과 `이름` 옵션이 표시되고, 다른 언어 사용자에게는 기본 영어 이름이 표시됩니다. 명령 이름의 길이와 사용 가능한 문자는 일반 명령과 동일한 제한을 따릅니다【104993650755089†L47-L112】.

## 지역화된 날짜와 숫자 표시

`locale` 모듈을 사용하면 숫자와 날짜를 지역화된 형식으로 표시할 수 있습니다. 예를 들어 천 단위 구분 기호와 날짜 포맷을 각 국가에 맞게 출력할 수 있습니다.

```python
import locale
locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')

number = 1234567.89
print(locale.format_string('%n', number))  # '1,234,567.89'와 같은 형식 출력
```

다만 서버가 지원하지 않는 로케일은 설정할 수 없으므로, 컨테이너나 운영체제에 필요한 로케일을 설치해야 합니다. Discord 메시지에서 날짜/시간을 표시할 때는 Discord의 타임스탬프 포맷(`<t:unix:s>`)을 사용하면 클라이언트가 자동으로 지역화하여 표시합니다.

## 요약

다국어 지원은 글로벌 커뮤니티의 참여를 높여 줍니다. `gettext`를 통해 코드의 문자열을 외부 번역 파일로 분리하고, 슬래시 명령의 이름과 설명을 `locale_str` 매개변수로 현지화하세요. 또한 숫자와 날짜를 로케일에 맞춰 형식화하여 사용자에게 친숙한 인터페이스를 제공할 수 있습니다.

