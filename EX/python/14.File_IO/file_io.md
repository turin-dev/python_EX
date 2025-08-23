---

# 파일 입출력

## 파일 열기와 닫기

- `open(파일명, 모드, encoding)` 함수를 이용해 파일을 열 수 있습니다.
- 모드: `r`(읽기), `w`(쓰기; 기존 내용을 덮어씀), `a`(추가), `b`(바이너리), `t`(텍스트; 기본값), `+`(읽기/쓰기)을 조합하여 사용합니다.
- 작업이 끝나면 `close()`를 호출하여 파일을 닫아야 합니다.

```python
f = open("example.txt", "w", encoding="utf-8")
f.write("Hello, file!\n")
f.close()
```

## with 문을 이용한 파일 관리

- `with` 문을 사용하면 파일을 열고 블록이 끝날 때 자동으로 닫아줍니다. 예외가 발생하더라도 안전하게 리소스를 해제합니다.

```python
with open("example.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

## 읽기 메서드

- `read()` : 전체 파일 내용을 문자열로 읽어옵니다.
- `readline()` : 한 줄씩 읽습니다.
- `readlines()` : 모든 줄을 리스트로 반환합니다.

## 파일 쓰기와 추가

- `w` 모드는 파일을 새로 만들거나 기존 파일을 덮어쓰고, `a` 모드는 파일 끝에 내용을 추가합니다.

```python
with open("log.txt", "a", encoding="utf-8") as log_file:
    log_file.write("새로운 로그\n")
```

## 요약

파일 입출력은 `open()` 함수와 적절한 모드를 사용하여 수행할 수 있습니다. `with` 문을 사용하면 파일을 안전하게 처리할 수 있으며, 다양한 읽기/쓰기 메서드로 파일 데이터를 다룰 수 있습니다.

## 추가 설명

### 바이너리 파일과 버퍼 제어

바이너리 데이터를 다루기 위해서는 모드에 `b`를 추가합니다. 예를 들어 이미지나 오디오 파일을 읽을 때 `open('image.png', 'rb')`와 같이 사용합니다. `read()`와 `write()`는 바이트 객체를 반환하거나 요구합니다.

파일 객체는 현재 위치를 나타내는 커서를 유지합니다. `tell()`로 현재 위치를 알 수 있고 `seek(offset, whence)`로 위치를 이동할 수 있습니다. `seek(0)`은 파일의 처음으로 이동하고, `seek(0, 2)`는 끝으로 이동합니다.

### 줄별 읽기와 이터레이터 프로토콜

큰 파일을 한 번에 읽는 것은 메모리 문제를 일으킬 수 있습니다. 파일 객체는 자체적으로 이터레이터를 제공하므로 `for line in f` 형태로 한 줄씩 읽을 수 있습니다. `readline()`과 `readlines()`보다 효율적이며, `strip()`을 사용해 줄바꿈 문자를 제거할 수 있습니다.

```python
with open('data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())
```

### 기타 모듈: pathlib, csv, json

`pathlib` 모듈은 객체 지향적으로 파일 시스템 경로를 다루게 해줍니다. `csv` 모듈은 쉼표 구분 값 파일을 읽고 쓰기 위한 도구를 제공하며, `json` 모듈은 JSON 형식의 데이터를 직렬화하고 역직렬화하는 기능을 제공합니다. 또한 임시 파일을 생성할 때는 `tempfile` 모듈의 `NamedTemporaryFile`이나 `TemporaryDirectory`를 사용할 수 있습니다.

### 예외 처리

파일 입출력 중에는 파일을 찾을 수 없거나 권한이 없는 등 다양한 예외가 발생할 수 있으므로 `try`/`except` 구문과 함께 사용하는 것이 좋습니다. 예외 처리에 대해서는 예외 처리 장에서 더 자세히 다룹니다.