# 제69장 – 명령줄 인자 파싱

대부분의 파이썬 스크립트는 동작을 제어하기 위한 명령줄 인자를 받습니다. `argparse` 모듈은 옵션을 정의하고 인자를 파싱하며 자동으로 도움말 메시지를 생성하기 쉽게 만듭니다. 매우 간단한 경우에는 `sys.argv`를 직접 사용하거나 `getopt`로 Unix 스타일 옵션을 파싱할 수도 있습니다. 명령줄 인자는 문자열이므로 많은 OS API가 다른 문자열 기반 입력과 동일하게 취급합니다【549557713116431†L69-L76】.

## `argparse` 사용하기

`argparse`를 사용하려면 `ArgumentParser` 객체를 생성하고, `add_argument()`로 인자와 옵션을 정의한 다음 `parse_args()`를 호출하여 각 인자에 해당하는 속성이 있는 객체를 반환받습니다. 파서 객체는 `-h/--help` 옵션을 자동으로 처리하여 사용법을 출력합니다.

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Demo script")
    parser.add_argument("filename", help="Input file name")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--count", type=int, default=1, help="Number of repetitions")
    args = parser.parse_args()
    for i in range(args.count):
        if args.verbose:
            print(f"Processing {args.filename} (iteration {i+1})")
        else:
            print(f"Processing {args.filename}")

if __name__ == "__main__":
    main()
```

## 원시 인자 접근하기

`sys.argv` 리스트에는 프로그램 이름과 이후 인자가 순서대로 포함됩니다. 매우 간단한 스크립트이거나 인자 파싱을 완전히 제어해야 하는 경우에 직접 사용할 수 있습니다.

```python
import sys

print("Program name:", sys.argv[0])
print("Arguments:", sys.argv[1:])
```

## `getopt`로 단순 옵션 파싱

Unix 스타일 옵션 파싱을 위해 `getopt.getopt(args, shortopts, longopts)`는 `(옵션, 값)` 쌍 목록과 남은 인자를 반환합니다. `argparse`보다 유연성은 떨어지지만 작은 스크립트에 적합할 수 있습니다.

## 요약

견고한 명령줄 파싱과 자동 도움말 메시지를 위해 `argparse`를 사용하세요. 간단한 스크립트에서는 `sys.argv`로 인자를 직접 접근하거나 `getopt`로 옵션을 처리할 수 있습니다. 명령줄 인자는 문자열이므로 필요한 유형으로 변환해야 합니다【549557713116431†L69-L76】.