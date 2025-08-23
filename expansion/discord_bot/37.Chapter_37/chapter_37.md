# 37장 – 설정 관리와 환경 변수

봇의 설정값을 소스 코드와 분리해 관리하는 것이 좋습니다. 예를 들어 봇의 접두사(prefix), 관리자 ID, API 키 등을 하드코딩하지 않고 설정 파일이나 환경 변수로 추출하면 유지보수가 쉬워집니다. Python에는 `configparser` 모듈이 INI 스타일의 설정 파일을 읽고 쓸 수 있는 클래스를 제공합니다【257164874177851†L96-L166】.

## `configparser` 사용법

설정 파일을 만들 때는 `[섹션]` 헤더와 `키=값` 쌍으로 정의합니다. 예시 `config.ini` 파일은 다음과 같습니다.

```
[bot]
prefix = !
owner_id = 123456789012345678

[api]
weather_key = YOUR_WEATHER_API_KEY
```

이 파일을 읽어 봇 설정으로 적용하려면 다음과 같이 합니다.

```python
import configparser

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

prefix = config.get("bot", "prefix", fallback="!")
owner_id = config.getint("bot", "owner_id")
weather_key = config.get("api", "weather_key")
```

`fallback` 매개변수는 값이 없을 때 기본값을 지정합니다. 변경된 설정을 저장하려면 `config.set()`과 `write()` 메서드를 사용합니다.

```python
config.set("bot", "prefix", "?")
with open("config.ini", "w", encoding="utf-8") as f:
    config.write(f)
```

## 환경 변수로 비밀 관리

민감한 값은 설정 파일 대신 환경 변수로 관리해야 합니다. 파이썬에서 환경 변수를 읽으려면 `os.environ.get()`을 사용하며, 기본값이 필요하면 두 번째 인자를 전달합니다【549557713116431†L69-L76】. `.env` 파일을 사용하는 경우 `python-dotenv` 패키지의 `load_dotenv()` 함수로 로드할 수 있습니다.

## 요약

`configparser`를 통해 봇 설정을 깔끔하게 분리하고, 환경 변수로 비밀을 관리하여 보안을 강화하세요. 설정 값을 하드코딩하지 않으면 배포 환경과 개발 환경을 쉽게 분리하고, 여러 봇 인스턴스를 구성하는 데도 유용합니다.

