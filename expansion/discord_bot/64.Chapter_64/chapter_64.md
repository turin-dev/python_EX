# 환경 변수와 비밀 관리

디스코드 봇을 배포할 때는 토큰과 데이터베이스 비밀번호 같은 비밀 값을 코드에 하드코딩하지 않고 안전하게 관리해야 합니다. 이를 위해 **환경 변수**와 **비밀 관리 도구**를 활용할 수 있습니다. 이 장에서는 `.env` 파일과 `python-dotenv`를 사용하는 방법, 그리고 운영 환경에서 안전하게 비밀을 주입하는 전략을 설명합니다.

## .env 파일과 python-dotenv

프로젝트 루트에 `.env` 파일을 두고 다음과 같이 키-값 쌍을 저장할 수 있습니다:

```
DISCORD_TOKEN=your-token-here
DATABASE_URL=postgresql://user:pass@localhost/db
```

`python-dotenv` 패키지를 설치하면 이 파일을 쉽게 로드할 수 있습니다:

```python
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
db_url = os.getenv("DATABASE_URL")
```

이렇게 하면 코드를 변경하지 않고도 환경마다 다른 값을 설정할 수 있습니다. `.env` 파일은 버전 관리에서 제외(`.gitignore`)하여 외부에 노출되지 않도록 합니다.

## 운영 환경에서의 비밀 주입

컨테이너 오케스트레이션 플랫폼(예: Docker Compose, Kubernetes)에서는 환경 변수를 통해 비밀을 주입할 수 있습니다. 또한 GitHub Actions에서는 Secrets 기능을 사용해 워크플로 내에서 비밀 값을 사용할 수 있습니다. 예를 들어 `docker run` 명령에서 `-e DISCORD_TOKEN=$DISCORD_TOKEN` 옵션으로 토큰을 전달하면 컨테이너 내에서 해당 값이 읽힙니다.

## 주의사항

- 비밀 값은 로그나 오류 메시지에 노출되지 않도록 주의합니다.
- 테스트 환경과 운영 환경에서 서로 다른 토큰을 사용하여 실수로 실제 서버에 영향을 주지 않도록 합니다.
- 환경 변수 이름은 모두 대문자로 작성하고, 의미를 명확히 합니다.

환경 변수를 통해 비밀을 관리하면 코드의 보안을 높이고, 다른 환경에서 봇을 쉽게 배포할 수 있습니다.

