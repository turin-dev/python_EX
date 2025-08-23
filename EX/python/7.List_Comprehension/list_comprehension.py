# 리스트와 컴프리헨션 예제

# 기본 리스트 메서드 사용
fruits = ['apple', 'banana', 'cherry']
fruits.append('orange')
fruits.remove('banana')
print('fruits:', fruits)

# 리스트 컴프리헨션을 이용한 제곱 리스트 생성
squares = [x**2 for x in range(10)]
print('squares:', squares)

# 조건이 있는 컴프리헨션: 짝수의 제곱만
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print('even squares:', even_squares)

# 집합과 딕셔너리 컴프리헨션 예제
unique_letters = {letter for letter in 'hello world' if letter.isalpha()}
print('unique letters set:', unique_letters)

squares_dict = {x: x**2 for x in range(5)}
print('squares dict:', squares_dict)

# 할당식을 이용한 컴프리헨션
allowed_names = {'python', 'java', 'rust'}
names = ['Python', 'JAVA', 'go', 'rust']
cleaned = [clean.title() for name in names if (clean := name.lower()) in allowed_names]
print('cleaned names:', cleaned)

# 중첩 컴프리헨션: 두 리스트의 모든 조합
colors = ['red', 'green']
objects = ['apple', 'leaf']
pairs = [(c, o) for c in colors for o in objects]
print('pairs:', pairs)

# 행렬 전치: 중첩 컴프리헨션과 zip 사용 비교
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print('transposed:', transposed)

transposed2 = list(zip(*matrix))
print('transposed2 using zip:', transposed2)

# 딕셔너리와 집합 컴프리헨션
words = ['python', 'java', 'c']
length_map = {w: len(w) for w in words}
print('length map:', length_map)

vowels = {ch for ch in 'Hello World' if ch.lower() in 'aeiou'}
print('vowels set:', vowels)

# 제너레이터 표현식 예제
squares_gen = (x**2 for x in range(10))
first_three = [next(squares_gen) for _ in range(3)]
print('generator first 3 values:', first_three)