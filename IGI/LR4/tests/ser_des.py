import pickle
import cloudpickle
import csv
import json
import shelve

# Различные возможности для сериализации/десериализации

class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    #def __dict__(self):
    #    return {"name": self.__name, "age": self.__age}

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age


person = Person("Jack", 18)

# МОДУЛЬ PICKLE
person_bytes = pickle.dumps(person)
print("Serialized Person: ")
print(person_bytes)
person = pickle.loads(person_bytes)
print("Deserialized Person: ")
print(person.name, person.age)

# Серализуем и десериализуем лямбда-функцию
my_lambda = lambda x: x+1
lambda_bytes = cloudpickle.dumps(my_lambda)
print("Serialized lambda:")
print(lambda_bytes)
my_lambda = cloudpickle.loads(lambda_bytes)
print("Deserialized lambda for x=1:")
print(my_lambda(1))

# МОДУЛЬ CSV
phones = { "Xiaomi":  ["Redmi7", 320, "New"],
           "Samsung": ["Galaxy", 550, "Old"],
           "Huawei":  ["P20",    420, "New"] }

with open("output.csv", "w") as file:
    dict_writer = csv.DictWriter(file, fieldnames=["Producer", "Model", "Price", "State"])
    dict_writer.writeheader() # Записали заголовки
    for producer, values in phones.items():
        dict_writer.writerow(dict(Producer = producer, Model=values[0], Price=values[1], State=values[2]))


# МОДУЛЬ JSON
# Для сериализации объекта необходимо определить метод __dict__ (возвращающий атрибуты класса в виде словаря)
print("Serialized person with JSON:")
print(json.dumps({"name": person.name, "age": person.age}, indent=3))


# МОДУЛЬ SHELVE
my_shelve = shelve.open("shelve_test")
my_shelve["Liza"] = "Sytsevich"
my_shelve["some_password"] = 12345
my_shelve["secret"] = "Hello, world!"

# my_sehlve в таком случае является абстракцией (что-то вроде словаря: есть ключи, значения и т.д.)
print(my_shelve["Liza"])
print(my_shelve.get("some_password", "No password"))
print(my_shelve)
print(my_shelve.items())

my_shelve.clear()
my_shelve.close()