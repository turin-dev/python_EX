"""예제 27: JSON과 CSV 모듈을 사용한 데이터 직렬화.

이 스크립트는 json.dumps/json.loads를 사용해 파이썬 객체를 JSON으로 직렬화하고
역직렬화하는 방법과, csv.DictWriter/DictReader를 사용해 CSV 파일을 읽고 쓰는
방법을 보여 준다.
"""

import json
import csv


def demo_json() -> None:
    data = {
        'title': 'Python Tutorial',
        'chapters': [1, 2, 3],
        'released': True,
    }
    # 객체를 JSON 문자열로 변환
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    print('Serialized JSON:\n', json_str)
    # 다시 객체로 변환
    obj = json.loads(json_str)
    print('Deserialized:', obj)

    # 파일에 저장
    with open('demo.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    # 파일에서 읽기
    with open('demo.json', 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    print('Loaded from file:', loaded)


def demo_csv() -> None:
    rows = [
        {'name': 'Alice', 'score': 85},
        {'name': 'Bob', 'score': 92},
        {'name': 'Charlie', 'score': 78},
    ]
    # CSV 파일에 쓰기
    with open('scores.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'score'])
        writer.writeheader()
        writer.writerows(rows)
    # CSV 파일 읽기
    with open('scores.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"{row['name']} scored {row['score']}")


if __name__ == '__main__':
    demo_json()
    print('---')
    demo_csv()