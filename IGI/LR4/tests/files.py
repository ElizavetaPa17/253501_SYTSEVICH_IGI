# Различные операции с файлами

# Менеджер контекста самостоятельно закрывает файл при выходе из области видимости
with open("../school", "rb") as file:
    print(f"Имя файла: {file.name}\n"
          f"Режим: {file.mode}\n")

    # Можно прочитать байты (только в бинарном режиме!)
    file_bytes = bytearray()
    file.readinto(file_bytes)


# Запишем данные в бинарный файл и считаем их
with open("file_test.txt", "wb+") as file:
    file.write(bytes("Hello, world!".encode("utf-8")))

    # Сбрасываем буферы
    file.flush()

    test = file.read(len("Hello, world!")).decode("utf-8")
    print(f"read from binary file: {test}")


with open("../task2_source.txt", "r") as file:
    # Считываем содержимое в виде списка строк
    lines = file.readlines()
    print(lines)


# Используем print нестандартным способом
with open("print_test.txt", "w") as file:
    print("Hello, world!", file=file)
