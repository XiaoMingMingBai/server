numbers = [1, 2, 3, 4, 5]

squared_numbers = map(lambda x: x ** 2, numbers)

squared_list = [num for num in squared_numbers]

print(squared_list)