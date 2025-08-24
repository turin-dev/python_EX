# 27. 데이터 직렬화: JSON과 CSV

파이썬 표준 라이브러리는 다양한 데이터 형식을 직렬화·역직렬화할 수 있는 모듈을 제공한다. 그 중 **`json`** 모듈은 자바스크립트 객체 표기법(JSON) 형태의 문자열을 읽고 쓰며, **`csv`** 모듈은 스프레드시트에서 흔히 사용하는 CSV 형식의 데이터를 읽고 쓴다.

## JSON 모듈

`json` 모듈은 [RFC 7159](https://datatracker.ietf.org/doc/html/rfc7159)에 정의된 JSON 규격을 구현한다. 문서에 따르면 JSON은 자바스크립트 객체 리터럴에서 영감을 받은 가벼운 데이터 교환 형식으로, `json.dumps()`와 `json.loads()`를 통해 파이썬 객체와 JSON 문자열을 상호 변환할 수 있다【312710426547340†L66-L76】. 경고로, **신뢰할 수 없는 데이터의 디코딩은 CPU와 메모리 자원을 과도하게 소비할 수 있으므로 주의해야 한다**【312710426547340†L72-L82】.

```python
import json

data = {'name': 'Alice', 'age': 30, 'skills': ['Python', 'SQL']}

# 직렬화: 파이썬 객체 → JSON 문자열
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)  # {"name": "Alice", "age": 30, "skills": ["Python", "SQL"]}

# 역직렬화: JSON 문자열 → 파이썬 객체
obj = json.loads(json_str)
print(obj['skills'])  # ['Python', 'SQL']

# 파일 단위로 저장과 읽기
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open('data.json', 'r', encoding='utf-8') as f:
    loaded = json.load(f)
```

`json.dumps()`는 `ensure_ascii=False` 옵션으로 한글 등 비ASCII 문자를 제대로 인코딩할 수 있고, `indent` 매개변수로 사람이 읽기 쉬운 서식을 제공한다. `json.loads()`는 문자열을 파이썬 객체로 변환하며, `object_hook`나 `parse_float` 등을 사용하면 사용자 정의 객체 변환이 가능하다【312710426547340†L144-L167】.

## CSV 모듈

CSV(Comma Separated Values) 형식은 데이터베이스와 스프레드시트에서 가장 널리 사용되는 교환 형식이다. Python의 `csv` 모듈은 **엑셀과 호환되는 형식으로 데이터를 읽고 쓸 수 있도록 해 주며**, `csv.reader`와 `csv.writer`를 통해 리스트 형태의 데이터를 다룬다【268712698667224†L60-L76】. `DictReader`와 `DictWriter`를 사용하면 각 행을 딕셔너리로 처리할 수 있어 컬럼 이름으로 접근하기 편리하다【268712698667224†L78-L80】.

```python
import csv

rows = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
]

# 쓰기: 딕셔너리 리스트 → CSV 파일
with open('people.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age'])
    writer.writeheader()
    writer.writerows(rows)

# 읽기: CSV 파일 → 딕셔너리 리스트
with open('people.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])
```

`csv.reader()`와 `csv.writer()`는 리스트 형태의 행(row)을 다루며, 파일을 열 때는 `newline=''` 옵션을 지정하는 것이 호환성 측면에서 권장된다【268712698667224†L92-L106】. 구분자나 인코딩 등 세부 설정을 변경하여 다른 CSV 방식을 지원할 수도 있다.

JSON과 CSV는 범용성 높은 직렬화 포맷으로, 각각 키‑값 구조와 표 형태 데이터를 표현하는 데 적합하다. 필요에 따라 두 모듈을 적절히 선택하면 데이터를 손쉽게 저장하고 교환할 수 있다.