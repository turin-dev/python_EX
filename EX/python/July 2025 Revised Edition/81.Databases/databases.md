# 제81장 – 경량 데이터베이스 인터페이스

파이썬은 데이터를 영구적으로 저장하기 위한 간단한 내장 인터페이스를 제공합니다. `dbm` 계열 모듈(`dbm.ndbm`, `dbm.gnu`, `dbm.dumb`)은 디스크 파일을 기반으로 하는 키‑값 저장소를 구현합니다. 이들은 딕셔너리처럼 동작하지만 키와 값이 바이트 형태로 저장됩니다. 관계형 데이터를 위해 `sqlite3` 모듈은 DB‑API 2.0 사양을 준수하는 임베디드 SQL 데이터베이스 엔진을 제공합니다. SQLite는 서버가 필요 없는 가볍고 단일 파일 기반 데이터베이스입니다【232817957113109†L82-L92】.

## `dbm`을 이용한 키‑값 데이터베이스

`dbm.open(filename, flag='c')`를 호출하여 데이터베이스 파일을 엽니다. 반환된 객체는 딕셔너리 연산(`db[key]`, `db.keys()`)을 지원하지만, 키와 값은 바이트이거나 바이트로 변환 가능한 객체여야 합니다. `flag` 인자는 데이터베이스를 생성(`'c'`), 읽기 전용(`'r'`), 새로 생성(`'n'`) 또는 이미 존재해야 함(`'w'`)을 지정합니다. 작업이 끝나면 반드시 데이터베이스를 닫아야 합니다.

```python
import dbm

with dbm.open('prefs.db', 'c') as db:
    db[b'color'] = b'blue'
    db[b'size'] = b'large'
    print(list(db.keys()))  # [b'color', b'size']
    print(db[b'color'])    # b'blue'
```

## `sqlite3`를 이용한 임베디드 SQL

`sqlite3` 모듈은 SQLite 엔진에 대한 DB‑API 2.0 인터페이스를 제공합니다. SQLite는 데이터베이스 전체를 단일 파일에 저장하며 별도의 서버가 필요 없고, 중소 규모 애플리케이션에 적합합니다【232817957113109†L82-L92】. `sqlite3.connect(path)`로 연결을 생성하고, `conn.cursor()`로 커서를 가져온 후 `cursor.execute()`로 SQL 문을 실행합니다. 변경 사항을 저장하려면 `commit()`을 호출하고, 사용이 끝나면 `close()`를 호출합니다.

```python
import sqlite3

conn = sqlite3.connect('example.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
cur.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))
cur.execute('SELECT id, name FROM users')
print(cur.fetchall())
conn.commit()
conn.close()
```

## 요약

단순한 키‑값 저장소에는 `dbm` 모듈을, 단일 파일에 SQL 데이터베이스를 저장하려면 `sqlite3`를 사용하세요. 두 옵션 모두 파이썬 표준 라이브러리의 일부이며 외부 의존성이 필요 없습니다【232817957113109†L82-L92】.