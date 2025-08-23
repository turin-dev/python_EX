# 36장 – 배포와 호스팅 전략

개발한 디스코드 봇을 실제 서버에서 안정적으로 운영하려면 배포와 호스팅 전략을 고려해야 합니다. 클라우드 플랫폼(예: Heroku, AWS, Google Cloud)이나 가정용 서버를 사용할 수 있으며, 지속적인 실행, 자동 재시작, 보안 관리를 설계해야 합니다. Python 애플리케이션은 패키지 설치와 환경 변수 설정만으로 간편하게 배포할 수 있습니다.

## 환경 변수와 비밀 관리

봇 토큰과 API 키 등 민감한 정보는 코드에 직접 작성하지 말고 환경 변수로 관리하세요. Python에서 환경 변수를 읽으려면 `os.environ`을 사용합니다.

```python
import os

TOKEN = os.environ.get("DISCORD_TOKEN")
API_KEY = os.environ.get("MY_API_KEY")

if TOKEN is None:
    raise RuntimeError("DISCORD_TOKEN 환경 변수가 설정되어 있지 않습니다.")
```

`.env` 파일을 사용하여 개발 환경에서 변수를 관리할 수 있으며, `dotenv` 라이브러리를 설치해 자동으로 로드할 수 있습니다. 배포 환경에서는 호스팅 서비스의 환경 변수 설정 UI를 통해 값을 입력합니다.

## 프로세스 관리와 자동 재시작

봇을 지속적으로 실행하려면 프로세스 관리 도구를 사용해야 합니다. Linux 서버에서는 `systemd` 서비스 유닛 파일을 작성하여 봇을 데몬으로 실행하고, 크래시 시 자동 재시작하도록 설정할 수 있습니다. Heroku에서는 `Procfile`을 사용해 실행 명령을 정의하고, `worker` 타입으로 배포합니다. 아래는 단순한 `systemd` 유닛 예입니다.

```
[Unit]
Description=Discord Bot
After=network.target

[Service]
Type=simple
Environment="DISCORD_TOKEN=your_token"
WorkingDirectory=/opt/discordbot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

`Restart=always` 옵션은 프로세스가 종료될 때 자동으로 재시작하도록 합니다. 로그는 `journalctl`로 확인하거나 로그 파일을 별도로 설정할 수 있습니다.

## 컨테이너와 CI/CD

Docker와 같은 컨테이너 기술을 사용하면 애플리케이션과 모든 의존성을 이미지로 패키징할 수 있어 배포가 일관되고 반복 가능합니다. GitHub Actions를 이용해 커밋 또는 태그 발생 시 Docker 이미지를 빌드하고 배포하는 CI/CD 파이프라인을 구축할 수 있습니다. 또한 보안 업데이트를 위해 정기적으로 이미지 베이스를 갱신해야 합니다.

## 요약

배포는 봇의 안정성과 보안을 좌우합니다. 환경 변수로 비밀을 관리하고, 운영 환경에서는 프로세스 관리 도구로 자동 재시작을 구성하세요. 클라우드 서비스나 컨테이너를 활용해 손쉽게 배포하고, CI/CD 파이프라인을 구축해 업데이트를 자동화하면 생산성이 향상됩니다【549557713116431†L69-L76】.

