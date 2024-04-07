import random

# Инициализируем наш генератор случайных чисел
random.seed() # Аргумент не передан, так что используется системное время

# Генерируем случайное число из 8 бит
print(random.getrandbits(8))

# Генерируем случайные числа
print(random.randrange(0, 10, 1))
print(random.randint(-10, 10))
print(random.random())
print(random.uniform(-10, 10))

# Случайно выбираем элемент из последовательности
print(random.choice(["cat", "dog", "rabbit", "duck"]))

# Перемешиваем последовательность
seq = ["You win 3 dollars!", "You win 5 dollars", "You win 1 dollar!"]
random.shuffle(seq)
print(seq[0])