# 제70장 – 파일 유틸리티: 글로빙, 매칭 및 복사

파이썬은 파일을 찾고, 비교하며, 복사하는 데 유용한 모듈을 제공합니다. 이러한 유틸리티는 크로스 플랫폼 `os` 모듈을 기반으로 하며, 파일 관리 작업을 단순화하는 상위 수준 기능을 제공합니다【549557713116431†L69-L76】.

## `glob`와 `fnmatch`로 패턴 매칭

* **`glob`** – Unix 셸과 동일한 규칙에 따라 지정된 패턴과 일치하는 모든 경로 이름을 찾습니다. 패턴에는 `*`, `?`, 대괄호 안 문자 집합 등 와일드카드를 사용할 수 있습니다. `glob.glob(pattern)`은 일치하는 경로 목록을 반환합니다.
* **`fnmatch`** – 단일 파일 이름이 패턴과 일치하는지 테스트합니다. `fnmatch.fnmatch(filename, pattern)`이나 `fnmatch.filter(list, pattern)`을 사용하여 목록을 필터링할 수 있습니다.

```python
import glob
import fnmatch

# 현재 디렉터리의 모든 파이썬 파일 찾기
print(glob.glob("*.py"))

names = ["test.py", "data.txt", "script.sh"]
print(fnmatch.filter(names, "*.py"))  # ['test.py']
```

## 파일 비교 및 복사

* **`filecmp`** – 파일과 디렉터리를 얕은 또는 깊은 수준에서 비교합니다. `filecmp.cmp(f1, f2, shallow=True)`는 두 파일 내용이 동일한 경우 `True`를 반환합니다.
* **`shutil`** – 파일을 복사하고 이동하며 디렉터리를 삭제하거나 보관용 아카이브를 만들 수 있는 고수준 파일 연산 기능을 제공합니다. `shutil.copy()`, `copytree()`, `rmtree()`, `make_archive()` 등이 있습니다.

```python
import filecmp
import shutil

# 두 파일 비교
same = filecmp.cmp("file1.txt", "file2.txt", shallow=False)
print("Files identical?", same)

# 파일 복사
shutil.copy("file1.txt", "file1.bak")
```

## 요약

`glob`와 `fnmatch` 모듈을 사용하면 와일드카드 패턴으로 파일을 찾을 수 있습니다. `filecmp`는 파일 내용을 비교하고, `shutil`은 파일 복사, 이동 및 삭제 같은 작업을 처리합니다. 이러한 유틸리티는 하위 수준 `os` 함수의 보완재로서 파일 관리 작업을 쉽게 해 줍니다【549557713116431†L69-L76】.