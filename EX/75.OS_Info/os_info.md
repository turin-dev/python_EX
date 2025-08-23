# 제75장 – 런타임과 운영체제 정보 조사

소프트웨어를 이식 가능하고 적응력 있게 만들기 위해서는 현재 파이썬 런타임과 운영체제에 대한 정보를 발견해야 합니다. `sys`, `platform`, `os` 모듈은 인터프리터, 플랫폼, 환경에 대한 세부 정보를 제공합니다. `os` 모듈은 다양한 운영체제 기능에 대한 일관된 인터페이스를 제공하는 것이 목표입니다【549557713116431†L69-L76】.

## `sys` 모듈

`sys` 모듈은 인터프리터 전용 함수와 변수를 노출합니다:

* `sys.version` – 파이썬 버전 문자열
* `sys.platform` – 플랫폼 식별자(`'win32'`, `'linux'`, `'darwin'` 등)
* `sys.maxsize` – 이 플랫폼에서 파이썬 정수의 최대 값(근사값)
* `sys.path` – 모듈을 찾는 디렉터리 목록
* `sys.getsizeof(obj)` – 객체의 대략적인 바이트 크기

## `platform` 모듈

`platform` 모듈을 사용하면 운영체제와 하드웨어에 대한 사람이 읽을 수 있는 정보를 얻을 수 있습니다. `platform.system()`, `platform.release()`, `platform.machine()`, `platform.python_implementation()` 등 다양한 함수를 제공합니다.

```python
import platform

print(platform.system())         # 'Linux', 'Windows', 'Darwin' 등
print(platform.release())        # 커널 또는 OS 릴리스
print(platform.machine())        # CPU 아키텍처
print(platform.python_version()) # 파이썬 버전
```

## 환경과 구성

`os` 모듈은 `os.name`(`'posix'`, `'nt'` 등)과 Unix에서 `os.uname()`을 제공하여 저수준 시스템 정보를 제공합니다. 환경 변수는 `os.environ` 딕셔너리나 `os.getenv()` 함수를 통해 접근할 수 있습니다. 이러한 값을 확인하면 프로그램 동작을 조정하는 데 도움이 됩니다.

## 요약

`sys`는 인터프리터에 대한 세부 정보를, `platform`은 운영체제와 하드웨어에 대한 설명을, `os`는 저수준 이름과 환경 변수를 제공합니다. 이 모듈들을 활용하면 프로그램을 다양한 플랫폼과 버전에 적응시킬 수 있습니다【549557713116431†L69-L76】.