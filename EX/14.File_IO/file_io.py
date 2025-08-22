# 파일 입출력 예제

# 파일 쓰기
with open('example.txt', 'w', encoding='utf-8') as f:
    f.write('Hello, file!\n')

# 파일 읽기
with open('example.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print('file content:', content)

# 파일에 내용 추가
with open('example.txt', 'a', encoding='utf-8') as f:
    f.write('Another line\n')

# 한 줄씩 읽기
with open('example.txt', 'r', encoding='utf-8') as f:
    line1 = f.readline()
    line2 = f.readline()
    print('first line:', line1.strip())
    print('second line:', line2.strip())

# 바이너리 파일 쓰고 읽기
data_bytes = b'\x00\x01\x02'
with open('binary.bin', 'wb') as bf:
    bf.write(data_bytes)
with open('binary.bin', 'rb') as bf:
    content = bf.read()
    print('binary content:', content)

# seek와 tell 사용
with open('example.txt', 'r', encoding='utf-8') as f:
    pos = f.tell()
    print('initial position:', pos)
    f.seek(0, 2)  # 파일 끝으로 이동
    end_pos = f.tell()
    print('end position:', end_pos)

# 한 줄씩 이터레이션
with open('example.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print('iter line:', line.strip())

# pathlib 사용 예 (경로 조작)
from pathlib import Path
p = Path('example.txt')
print('file exists:', p.exists(), 'size:', p.stat().st_size)