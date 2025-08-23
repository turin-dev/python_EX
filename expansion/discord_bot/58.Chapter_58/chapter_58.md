# 배포: Docker와 CI/CD

봇을 안정적으로 배포하려면 런타임 환경을 고정하고 자동화된 배포 파이프라인을 구축하는 것이 좋습니다. 이 장에서는 **Docker** 컨테이너를 이용한 배포와 **GitHub Actions**를 활용한 CI/CD 설정 방법을 설명합니다.

## Docker로 배포하기

Docker는 애플리케이션과 그 의존성을 하나의 이미지로 패키징하여 어느 환경에서나 동일하게 실행할 수 있게 합니다. 디스코드 봇의 Dockerfile은 대체로 다음과 같이 구성됩니다:

```dockerfile
# 베이스 이미지 선택: 가벼운 Python 이미지를 사용
FROM python:3.12-slim AS base

# 작업 디렉터리 설정
WORKDIR /app

# 의존성 복사 및 설치
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# 소스 코드 복사
COPY . .

# 환경 변수 설정(예: 토큰)
ENV PYTHONUNBUFFERED=1

# 실행 명령
CMD ["python", "bot.py"]
```

이 Dockerfile은 `python:3.12-slim` 이미지를 기반으로 하고, Poetry를 사용해 의존성을 설치한 후 봇 코드를 실행합니다. 소스 코드를 복사하기 전에 종속성 파일만 복사해 Docker 레이어 캐시를 효율적으로 사용합니다. 실제 프로젝트에서는 `requirements.txt`를 직접 사용하거나 `pip install -r`로 대체할 수 있습니다.

컨테이너 빌드와 실행은 다음 명령으로 수행합니다:

```bash
docker build -t my-discord-bot .
docker run -e DISCORD_TOKEN=your_token_here my-discord-bot
```

## GitHub Actions로 CI/CD 구성

GitHub Actions를 활용하면 커밋 또는 태그 푸시 시 자동으로 빌드하고 배포할 수 있습니다. 아래는 Docker 이미지를 빌드하여 Docker Hub에 푸시하는 간단한 워크플로 예제입니다.

```yaml
name: Deploy Discord Bot

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/my-discord-bot:latest
```

위 워크플로는 `main` 브랜치에 푸시될 때마다 이미지를 빌드하고 Docker Hub에 푸시합니다. 비밀 값은 리포지토리 설정의 **Secrets**에서 등록해야 합니다. 배포 서버에서는 `docker pull`로 새 이미지를 가져와 재시작하는 스크립트를 작성할 수 있습니다.

## 요약

Docker를 사용하면 애플리케이션 환경을 일관되게 유지할 수 있고, GitHub Actions를 통해 변경 사항을 자동으로 빌드·배포할 수 있습니다. 토큰과 같은 민감한 정보는 환경 변수나 CI 서비스의 보안 저장소에 저장하여 코드에 노출되지 않도록 관리해야 합니다【257164874177851†L96-L166】.

