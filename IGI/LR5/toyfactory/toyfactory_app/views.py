from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *

# toyfactory - Домашняя страница
# toyfactory/toys - Список всех игрушек
# toyfactory/employees - Список всех сотрудников
# toyfactory/clients - Список всех клиентов
# toyfactory/orders - Список всех заказов
# toyfactory/promocodes - Список всех промокодов
# toyfactory/toys/<id> - Описание продукта
# toyfactory/employees<id> - Описание продукта
# toyfactory/clients/<id> - Описание клиента
# toyfactory/orders/<id> - Описание заказа
# toyfactory/promocode/<id> - Описание промокода


# Create your views here.


def index(request):
    return render(request, 'index.html')


def toys(request):
    return render(request, 'toys.html')


def employees(request):
    return render(request, 'employees.html')


def promocodes(request):
    return render(request, 'promocodes.html')


def reviews(request):
    return render(request, 'reviews.html')


def policy(request):
    return render(request, 'policy.html')


def vacations(request):
    return render(request, 'vacations.html')


def about(request):
    return render(request, 'about.html')


def termines(request):
    return render(request, 'termines.html')

