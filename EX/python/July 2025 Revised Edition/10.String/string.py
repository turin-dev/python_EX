# 문자열 다루기 예제

# 문자열 생성과 인덱싱
s = "Hello, Python"
print(s[0])    # H
print(s[7:])   # Python

# 문자열 메서드 사용
text = "  Python is Fun!  "
print(text.strip().lower())
print(text.replace("Fun", "Great"))

# f-문자열 포맷팅
name = "투린"
age = 14
print(f"{name}의 나이는 {age}살입니다.")

# 멀티라인 문자열
text_multi = """여러 줄
문자열 예시"""
print(text_multi)

# 문자열은 불변 - 새로운 문자열 생성
s2 = "hello"
# s2[0] = 'H'  # 불변 특성 때문에 수정 불가
s2 = 'H' + s2[1:]
print(s2)

# 검색과 카운팅
s3 = "banana"
print('find an:', s3.find('an'))
print('count a:', s3.count('a'))

# 분할과 결합
csv = "a,b,c"
fields = csv.split(',')
print('split:', fields)
print('joined with -:', '-'.join(fields))
print('splitlines:', "line1\nline2".splitlines())

# 정렬과 채우기
n = '42'
print('zfill:', n.zfill(5))
print('center:', 'Hi'.center(10, '*'))

# format() 메서드 사용
template = "{name} scored {score:.2f} points"
print(template.format(name='투린', score=97.5))

# 바이트 문자열과 인코딩/디코딩
data = '파이썬'.encode('utf-8')
print('encoded bytes:', data)
text = data.decode('utf-8')
print('decoded text:', text)