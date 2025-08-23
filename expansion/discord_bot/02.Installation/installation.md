# 설치 및 환경 구성

디스코드 봇을 개발하기 전에 Python 개발 환경을 준비하고 `discord.py` 라이브러리를 설치해야 합니다. 이 장에서는 **Python 설치**, **가상 환경 구성**, **패키지 설치**, 그리고 설치 확인 방법을 자세히 설명합니다. 또한 Intents 설정에 필요한 코드 작성법도 간단히 소개합니다.

## 1. Python과 pip 업데이트

`discord.py` 2.x 버전은 Python 3.8 이상을 요구합니다. 먼저 시스템에 설치된 Python 버전을 확인하고, 없다면 [Python 공식 웹사이트](https://www.python.org/)에서 최신 버전을 다운로드하여 설치합니다. `pip`는 Python 패키지 관리자로서, 다음 명령으로 최신 버전으로 업데이트합니다:

```bash
python3 -m pip install --upgrade pip
```

## 2. 가상 환경 생성

각 프로젝트마다 독립된 패키지 세트를 유지하려면 가상 환경을 사용하는 것이 좋습니다. 표준 라이브러리의 `venv` 모듈을 사용하면 손쉽게 가상 환경을 만들 수 있습니다. 프로젝트 폴더에서 다음을 실행하세요:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows의 경우 .venv\Scripts\activate
```

활성화 후 프롬프트 앞에 `(venv)`가 표시되며, 이 상태에서 설치한 패키지는 프로젝트에만 적용됩니다. 가상 환경을 비활성화하려면 `deactivate` 명령을 실행합니다.

## 3. discord.py 설치

가상 환경이 활성화된 상태에서 `discord.py`를 설치합니다. 최신 버전을 설치하려면 다음 명령을 사용합니다:

```bash
pip install -U discord.py
```

봇이 음성 채널에서 오디오를 송수신해야 한다면 추가 종속성이 필요한데, 이를 위해서는 `pip install -U "discord.py[voice]"` 명령을 사용합니다. `discord.py`는 PyPI에 패키지로 등록되어 있으므로 이 명령만으로 라이브러리와 그 의존성을 설치할 수 있습니다.

설치가 완료되면 Python 셸에서 다음과 같이 버전을 확인해 볼 수 있습니다:

```python
>>> import discord
>>> print(discord.__version__)
2.3.2  # 예시 출력: 사용 중인 버전을 확인하세요
```

## 4. Intents 준비 및 테스트 코드 실행

앞에서 언급한 것처럼, 봇이 메시지 내용 등 특정 이벤트를 수신하려면 **Intents**를 활성화해야 합니다【666664033931420†L32-L45】. 다음은 간단한 테스트 코드입니다. 디버깅 목적으로 작성했으며, 설치가 제대로 되었는지 확인할 수 있습니다:

```python
import os
import discord

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} 로깅인되었습니다!")

@bot.slash_command(description="안녕 메시지 전송")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("안녕하세요! 봇이 성공적으로 동작합니다.")

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))
```

이 코드를 실행하기 전에 `.env` 파일이나 환경 변수에 `DISCORD_TOKEN` 값을 설정해야 합니다. `bot.run()` 함수는 내부적으로 비동기 이벤트 루프를 생성하여 Discord 서버와의 연결을 유지합니다. 실행 후 콘솔에 봇 로그인 메시지가 출력되며, 서버에서 슬래시 명령 `/hello`를 호출해봄으로써 설치가 성공했는지 확인할 수 있습니다.

## 5. 추가 도구

- **poetry/pipenv**: 패키지 관리와 의존성 잠금을 위해 [Poetry](https://python-poetry.org/)나 [Pipenv](https://pipenv.pypa.io/)를 사용하면 프로젝트 간 충돌을 방지할 수 있습니다.
- **패키지 업데이트**: 주기적으로 `pip list --outdated` 명령으로 업데이트 가능한 패키지를 확인하고, `pip install --upgrade 패키지명`으로 최신 상태를 유지하세요.

이 장에서는 개발 환경 준비와 `discord.py` 설치 방법을 다뤘습니다. 다음 장에서는 클라이언트 객체와 이벤트 처리 방법을 깊이 있게 알아보겠습니다.



