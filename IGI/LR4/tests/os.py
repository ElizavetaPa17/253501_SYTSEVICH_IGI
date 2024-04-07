import os

# Различные операции с os

# Получаем текущую директорию
print(os.getcwd())

#Создаем директорию и удаляем ее
#os.mkdir("os_test")
#os.rmdir("os_test")

# Проверяем путь на то, указывает ли он на директорию
print("Is files.py a directory: ", os.path.isdir("files.py"))

# Меняем рабочую директорию и восстанавливаем ее
#os.chdir("os_test")
#print(os.getcwd())
#os.chdir("..")

# Генерируем дерево каталогов - вернется генератор, его можно перебирать
dirs_gen = os.walk("../")
for directory in dirs_gen:
    print(directory)

# Переименуем директорию
#os.rename("os_test", "new_os_test")

# Выведем информацию о файле (в виде структуры st_stat)
my_stat = os.stat("files.py")
print(f"Размер файла: {my_stat.st_size}\n")