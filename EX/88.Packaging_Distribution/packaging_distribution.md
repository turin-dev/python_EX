# 제88장 – 파이썬 프로젝트 패키징과 배포

파이썬 프로젝트를 패키징하면 설치 및 재사용이 가능해집니다. 현대적인 패키징은 `pyproject.toml` 파일을 기반으로 하며, 이 파일에서 빌드 요구사항과 메타데이터를 선언합니다. `pip`, `setuptools`, `flit`, `poetry` 같은 도구는 이 파일을 읽어 소스 배포판과 휠을 빌드합니다. 앞에서 소개한 `importlib.metadata` 모듈은 패키지를 임포트하지 않고도 메타데이터를 읽을 수 있습니다【491628540515688†L69-L84】.

## 패키지 구조 만들기

일반적인 프로젝트 구조는 다음과 같습니다:

```
myproject/
├── pyproject.toml
├── README.md
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
└── tests/
    └── test_module.py
```

`src` 레이아웃은 테스트가 소스 트리가 아닌 설치된 패키지를 임포트하게 합니다. `__init__.py` 파일은 `mypackage`를 패키지로 만듭니다.

## 메타데이터 선언

`pyproject.toml`에서 빌드 백엔드(예: `[build-system]`의 `requires = ["setuptools", "wheel"]`)와 프로젝트 메타데이터(이름, 버전, 설명, 작성자, 의존성)를 지정합니다.

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
description = "A sample package"
authors = [{ name = "Alice", email = "alice@example.com" }]
dependencies = ["requests"]
```

## 빌드 및 업로드

`build` 패키지를 설치한 후(`pip install build`) `python -m build`를 실행하면 `dist` 디렉터리에 소스 배포판과 휠이 생성됩니다. 패키지를 PyPI에 업로드하려면 `twine`을 사용합니다(`pip install twine`), 그 다음 `python -m twine upload dist/*`를 실행합니다. 업로드를 테스트하려면 테스트 PyPI(`https://test.pypi.org/`)를 사용할 수 있습니다.

## 요약

`pyproject.toml` 파일과 깔끔한 디렉터리 구조를 사용해 프로젝트를 패키징하세요. 빌드 도구를 사용해 휠과 소스 배포판을 생성하고, PyPI에 게시해 배포할 수 있습니다. 패키지 메타데이터는 `importlib.metadata`로 프로그램적으로 조회할 수 있습니다【491628540515688†L69-L84】.