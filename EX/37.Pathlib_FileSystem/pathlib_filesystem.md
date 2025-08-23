# Pathlib와 파일 시스템 작업

`pathlib` 모듈은 운영체제별 파일 경로를 객체 지향적으로 다룰 수 있도록 설계되었습니다. 이 모듈은 **순수 경로(pure paths)**와 **구체 경로(concrete paths)**로 나뉩니다. 순수 경로는 단순히 경로를 조작하는 데 사용되며 입출력 기능이 없고, 구체 경로는 파일 시스템 접근(파일 읽기/쓰기, 존재 여부 확인 등)을 제공합니다【600400567853462†L77-L81】. 대부분의 경우 플랫폼에 맞는 `Path` 클래스를 사용하면 됩니다【600400567853462†L89-L91】.

## 기본 사용법

* **경로 생성:** `from pathlib import Path` 후 `Path('경로')` 형태로 객체를 생성합니다. `/` 연산자를 사용하여 하위 경로를 간결하게 결합할 수 있습니다.
* **파일/디렉터리 탐색:** `Path.iterdir()`는 하위 항목을, `Path.glob('*.py')`와 `Path.rglob('**/*.py')`는 패턴에 맞는 파일을 반복합니다.
* **속성 검사:** `path.exists()`, `path.is_file()`, `path.is_dir()` 등의 메서드로 파일 유형과 존재 여부를 확인합니다.
* **읽기/쓰기:** `path.read_text()`, `path.write_text()`는 텍스트 파일을 간편하게 읽고 쓸 수 있으며, `read_bytes()`/`write_bytes()`는 바이너리 파일을 처리합니다.
* **경로 변환:** `path.resolve()`는 절대 경로를 반환하고, `path.name`, `path.stem`, `path.suffix` 속성으로 파일명과 확장자를 가져올 수 있습니다.

## 예제 패턴

`Path` 객체는 파일 시스템의 현재 디렉터리를 편리하게 순회할 수 있습니다. 다음과 같이 파이썬 파일을 재귀적으로 찾을 수 있습니다.

```python
from pathlib import Path

p = Path('.')
for py_file in p.rglob('*.py'):
    print(py_file)
```

또한 새 디렉터리를 만들고 파일을 저장하는 것도 간단합니다.

```python
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)
file_path = data_dir / 'hello.txt'
file_path.write_text('안녕하세요!')
print(file_path.read_text())
```

## 요약

`pathlib` 모듈은 문자열 기반 경로 조작보다 읽기 쉽고 오류를 줄이는 API를 제공합니다. 경로 조작과 파일 시스템 작업을 객체 지향적으로 처리하고자 할 때 `Path` 클래스를 활용하면 좋습니다【600400567853462†L77-L81】.

---

### 참고 문헌

1. `pathlib` 모듈은 운영체제별 의미를 가진 경로 클래스를 제공하며 순수 경로와 구체 경로로 나뉜다【600400567853462†L77-L81】.
2. 대부분의 경우 `Path` 클래스가 현재 플랫폼에 맞는 구체 경로 클래스를 사용하므로 적절하며, 순수 경로는 입출력 기능 없이 경로 계산에만 사용된다【600400567853462†L89-L91】.