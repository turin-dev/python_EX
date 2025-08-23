# 리스트 다루기 예제

# 리스트 생성 및 기본 인덱싱
numbers = [1, 2, 3]
mixed = [1, "Python", 3.14]
print('numbers[0]:', numbers[0], 'mixed[-1]:', mixed[-1])

# 리스트 메서드 예제
numbers2 = [3, 1, 4, 1, 5]
numbers2.append(9)
numbers2.remove(1)
numbers2.sort()
print('modified numbers2:', numbers2)

# 리스트 컴프리헨션을 이용한 변환
numbers3 = [1, 2, 3, 4]
squares = [x**2 for x in numbers3]
print('squares:', squares)

# 리스트가 가변 객체임을 보여주는 예
a = [1, 2, 3]
b = a  # 같은 리스트 객체를 참조
b.append(4)
print('a after b.append:', a)

# 기타 메서드와 슬라이스 대입 예제
nums = [1, 2, 2, 3]
print('count 2:', nums.count(2))
print('index of 3:', nums.index(3))

clone = nums.copy()
nums.clear()
print('after clear nums:', nums, 'clone:', clone)

lst = [0, 1, 2, 3, 4]
lst[1:3] = ['a', 'b']
print('after slice assignment:', lst)
del lst[2:4]
print('after del slice:', lst)

# sys.getsizeof 예제 (메모리 확인)
import sys
big_list = list(range(1000))
print('size of big_list:', sys.getsizeof(big_list), 'bytes')