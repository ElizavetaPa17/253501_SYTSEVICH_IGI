from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Permission, Group
from django.db import IntegrityError
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from .models import *
from .forms import *
from .constants import *
import pandas as pd
import datetime
import requests
import numpy as np
import dataframe_image as dfi
import seaborn as sns
import traceback
import logging
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from deep_translator import GoogleTranslator

# Create your views here.
def index(request):
    news_list = News.objects.all()
    news = None
    if news_list:
        news = news_list.last()

    # Используем наше API
    cat_fact = None
    dog_image = None

    #clients = Client.objects.all()
    #for client in clients:
    #    client.set_password('bz718nqf45')
    #    client.save()

    try:
        res = requests.get("https://catfact.ninja/fact").json()
        cat_fact = res['fact']
        cat_fact = GoogleTranslator(source='auto', target='ru').translate(cat_fact)

        res = requests.get("https://dog.ceo/api/breeds/image/random").json()
        dog_image = res['message']
    except Exception as ex:
        logging.error(traceback.format_exc())

    localtime = timezone.localtime(timezone.now()).time()
    localtimezone = get_current_timezone()

    return render(request, 'index.html', {'local_time': localtime,
                                          'local_timezone': localtimezone,
                                          'news' : news,
                                          'cat_fact' : cat_fact,
                                          'dog_image' : dog_image})

def news_list_view(request):
    news_list = News.objects.all()
    return render(request, 'news/list.html', {'news_list' : news_list})


def news_detail_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/detail.html', {'news' : news})


def promocodes_view(request, promocode_type=None):
    pr_type = None
    promocodes = Promocode.objects.all()
    pr_types = PromocodeType.objects.all()
    if promocode_type:
        pr_type = get_object_or_404(PromocodeType, slug=promocode_type)
        promocodes = promocodes.filter(promocode_type=pr_type)
    
    paginator = Paginator(promocodes, 5)
    page = request.GET.get('page')
    try:
        promocodes = paginator.page(page)
    except PageNotAnInteger:
        promocodes = paginator.page(1)
    except EmptyPage:
        promocodes = paginator.page(paginator.num_pages)
    return render(request, 'promocodes.html', {'pr_type'    : pr_type, 
                                               'pr_types'   : pr_types,
                                               'promocodes' : promocodes,
                                               'page' : page })


def feedbacks_view(request):
    feedbacks_list = Feedback.objects.all()
    paginator = Paginator(feedbacks_list, 5)
    page = request.GET.get('page')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        feedbacks = paginator.page(1)
    except EmptyPage:
        feedbacks = paginator.page(paginator.num_pages)
    return render(request, 'feedbacks/list.html', {'feedbacks' : feedbacks,
                                                   'page' : page,
                                                   'required_role' : CLIENT })


@permission_required("toyfactory_app.add_feedback", login_url='/account/login_client')
def add_feedback_view(request):
    errors = None
    if request.method == 'POST':
        try:
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback = feedback_form.save(commit=False)
                feedback.user = request.user
                feedback.date = datetime.date.today()
                feedback.save()
                logging.error(f'Создание отзыва клиентом {request.user}')
            else:
                errors = feedback_form.errors
                logging.info(f'Ошибка добавления отзыва: {errors}')
        except IntegrityError:
            errors = 'Вы уже написали свой отзыв.'

    feedback_form = FeedbackForm()
    return render(request, 'feedbacks/form.html', {'feedback_form' : feedback_form, 
                                                   'errors' : errors})

def policy_view(request):
    return render(request, 'policy.html')


def vacations_view(request):
    vacations_list = Vacation.objects.all()
    paginator = Paginator(vacations_list, 5)
    page = request.GET.get('page')
    try:
        vacations = paginator.page(page)
    except PageNotAnInteger:
        vacations = paginator.page(1)
    except EmptyPage:
        vacations = paginator.page(paginator.num_pages)
    return render(request, 'vacations.html', {'vacations' : vacations,
                                              'page' : page})


def about_view(request):
    company = Company.objects.all().first()
    return render(request, 'about.html', {'company' : company})


@login_required(login_url='/account/login_client')
def about_employees_view(request):
    employees_list = Employee.objects.all()
    paginator = Paginator(employees_list, 5)
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        temployees = paginator.page(paginator.num_pages)
    return render(request, 'toyfactory_app/employee_list.html', {'employee_list' : employees})


@login_required(login_url='/account/login_client')
def about_employee_detail_view(request, pk=None):
    employee = Employee.objects.all().filter(pk=pk).first()
    return render(request, 'toyfactory_app/employee_detail.html', {'employee' : employee})


def termines_view(request):
    termines_list = TermsDictionary.objects.all()
    paginator = Paginator(termines_list, 5)
    page = request.GET.get('page')
    try:
        termines = paginator.page(page)
    except PageNotAnInteger:
        termines = paginator.page(1)
    except EmptyPage:
        termines = paginator.page(paginator.num_pages)
    return render(request, 'termines.html', {'termines' : termines})


def register_client_view(request):
    errors = None
    if request.method == 'POST':
        client_form = ClientRegistrationForm(request.POST)
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.save()
            client_group = Group.objects.get(name='Клиенты')
            client_group.user_set.add(client)

            logging.error(f'Ошибка регистрации клиента с почтой {client_form.cleaned_data.get("email")}')
            return HttpResponseRedirect(reverse('login_client'))
        else:
            errors = client_form.errors
            logging.info(f'Ошибка регистрации клиента: {errors}')

    client_form = ClientRegistrationForm()
    return render(request, 'accounts/register_client.html', {'client_form' : client_form,
                                                             'errors' : errors })


def login_client_view(request):
    error = None
    errors = None
    if request.method == 'POST':
        client_form = ClientLoginForm(request.POST)
        if client_form.is_valid():
            first_name = client_form.cleaned_data.get('first_name')
            last_name = client_form.cleaned_data.get('last_name')
            password = client_form.cleaned_data.get('password1')
            user = authenticate(first_name=first_name, 
                                last_name=last_name,
                                password=password)
            if user and user.role == CLIENT:
                login(request, user)
                logging.info(f'Авторизация клиента с почтой {user.email}')
                return HttpResponseRedirect(reverse('index'))
            else:
                error = 'Клиент с такими данными не найден.'
                logging.info(f'Попытка авторизации клиента с несуществующими данными.')
        else:
            errors = client_form.errors
            logging.info(f'Ошибка регистрации клиента: {errors}')
    client_form = ClientLoginForm()
    return render(request, 'accounts/login_client.html', {'client_form' : client_form,
                                                          'errors' : errors,
                                                          'error' : error})
                

def login_employee_view(request):
    error = None
    errors = None
    if request.method == 'POST':
        employee_form = EmployeeLoginForm(request.POST)
        if employee_form.is_valid():
            first_name = employee_form.cleaned_data.get('first_name')
            last_name = employee_form.cleaned_data.get('last_name')
            password = employee_form.cleaned_data.get('password1')
            employee = authenticate(first_name=first_name,
                                    last_name=last_name, 
                                    password=password)
            if employee and employee.role == EMPLOYEE:
                login(request, employee)
                logging.info(f'Авторизация сотрудника с почтой {employee.email}')
                return HttpResponseRedirect(reverse('index'))
            else:
                error = 'Сотрудник с такими данными не найден.'
                logging.info(f'Ошибка регистрации сотрудника: {errors}')
        else:
            errors = employee_form.errors
    employee_form = EmployeeLoginForm()
    return render(request, 'accounts/login_employee.html', {'employee_form' : employee_form,
                                                            'errors' : errors, 
                                                            'error' : error})

@login_required(login_url='/account/login_client')
def update_profile_view(request, pk):
    errors = None
    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            logging.info(f'Обновления профиля пользователем {request.user}')
            return HttpResponseRedirect(reverse('login_client'))
        else:
            errors = profile_form.errors
            logging.info(f'Попытка сохранения профиля с невалидными полями')
    profile_form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/update_profile.html', {'profile_form' :  profile_form,
                                                            'errors' : errors})


@login_required(login_url='/account/login_client')
def logout_view(request):
    logout(request)
    logging.info(f'Выход из аккаунта пользователем {request.user}')
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/account/login_client')
def profile_view(request, pk):
    return render(request, 'accounts/profile.html', {'user' : request.user})


def toys_list_view(request, toy_type=None):
    ttype = None
    toys = Toy.objects.all()
    toy_types = ToyType.objects.all()
    if toy_type:
        ttype = get_object_or_404(ToyType, slug=toy_type)
        toys = toys.filter(toy_type=ttype)
    
    ordering = request.GET.get('orderby')
    if (ordering):
        if (ordering == 'По возрастанию цены'):
            toys = toys.order_by('price')
        elif (ordering == 'По убыванию цены'):
            toys = toys.order_by('-price')

    paginator = Paginator(toys, 5)
    page = request.GET.get('page')
    try:
        toys = paginator.page(page)
    except PageNotAnInteger:
        toys = paginator.page(1)
    except EmptyPage:
        toys = paginator.page(paginator.num_pages)
    
    pickuppoints = PickUpPoints.objects.all()
    return render(request, 'toy/list.html', {'ttype'  : ttype, 
                                             'ttypes' : toy_types,
                                             'toys' : toys,
                                             'page' : page,
                                             'pickuppoints' :  pickuppoints})


def toy_details_view(request, pk):
    toy = get_object_or_404(Toy, pk=pk)
    return render(request, 'toy/detail.html', { 'toy' : toy ,
                                                'required_role' : CLIENT})


@permission_required("toyfactory_app.add_order", login_url="/account/login_client")
def create_order_view(request, pk):
    errors = None
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)

            order.order_date = datetime.date.today()
            order.finish_date = datetime.date.today() + datetime.timedelta(days=3)
            order.client = get_object_or_404(Client, pk=request.user.pk)
            order.toy = get_object_or_404(Toy, pk=pk)
            order.total_price = order.toy.price * order_form.cleaned_data['toy_count'] * (1 - order_form.cleaned_data['promocodes'].discount / 100)
            order.save()

            logging.error(f'Создание заказа клиентом {request.user}')
            return HttpResponseRedirect(reverse('toys_list'))
        else:
            errors = order_form.errors
            logging.info(f'Попытка создания заказа с невалидными полями.')
    order_form = OrderForm()
    return render(request, 'toy/create_order.html', {'order_form' :  order_form,
                                                     'errors' : errors})


@permission_required("toyfactory_app.view_client", login_url="/account/login_employee")
def employee_clients_list_view(request):
    clients = UsersRelations.objects.all().filter(user_owner=request.user)

    paginator = Paginator(clients, 5)
    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    return render(request, 'clients/my_clients.html', {'clients' : clients,
                                                        'page' : page})


@permission_required("toyfactory_app.view_order", login_url="/account/login_employee")
def client_orders_view(request, pk=None):
    client = Client.objects.all().filter(pk=pk).first()
    orders = Order.objects.all().filter(client=client)
    
    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(request, 'clients/client_orders.html', {'client' : client,
                                                          'orders' : orders,
                                                          'page' : page})


@permission_required("toyfactory_app.view_order", login_url='/account/login_client')
def my_orders_view(request):
    client = Client.objects.all().filter(pk=request.user.pk).first()
    orders = Order.objects.all().filter(client=client)

    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(request, 'clients/my_orders.html', {'client' : client,
                                                      'orders' : orders,
                                                      'page' : page})


@permission_required("toyfactory_app.add_employee", login_url='/account/login_employee')
def statistics_view(request):
    return render(request, 'statistics/index.html')


@permission_required("toyfactory_app.add_employee", login_url='/account/login_employee')
def statistics_price_view(request):
    toys = Toy.objects.all()
    logging.debug('Статистика цен создана и сохранена.')

    return render(request, 'statistics/price_list.html', {'toys' : toys})


@permission_required("toyfactory_app.add_employee", login_url='/account/login_employee')
def statistics_clients_view(request):
    clients = Client.objects.all()
    towns = []
    ages = []
    fl_names = []
    for client in clients:
        if client.is_staff == False:
            towns.append(client.town)
            fl_names.append(client.first_name + ' ' + client.last_name)
            ages.append(datetime.datetime.today().year - client.birthday.year)

    df = pd.DataFrame({
        'Имя' : fl_names,
        'Город' : towns
    }, )

    # Группировка по городам
    df = df.rename(columns={'Город' : 'Город', 'Имя' : 'Количество проживающих'})
    fig = df.groupby('Город').count().plot(kind='barh', figsize=(15,7))
    fig.get_figure().savefig('media/images/clients_per_town.png')

    # Информация о возрасте
    df = pd.DataFrame({
        'Имя' : fl_names,
        'Возраст' : ages
    })

    df = df.rename(columns={'Имя' : 'Количество', 'Возраст' : 'Возраст'})
    df.groupby('Возраст').count().plot().get_figure().savefig('media/images/clients_ages.png')

    average_age = round(df['Возраст'].mean(), 2)
    max_age = df['Возраст'].max()
    min_age = df['Возраст'].min()

    logging.debug('Статистика клиентов создана и сохранена.')

    return render(request, 'statistics/clients_town_list.html', {'average_age' : average_age,
                                                                 'max_age' : max_age,
                                                                 'min_age' : min_age})


@permission_required("toyfactory_app.add_employee", login_url='/account/login_employee')
def statistics_toy_view(request):
    toys = Toy.objects.all()

    toy_names = []
    toy_type_names = []
    toy_prices = []

    for toy in toys:
        toy_names.append(toy.name)
        toy_type_names.append(toy.toy_type.name)
        toy_prices.append(toy.price)

    df = pd.DataFrame({
        'Наименование игрушки' : toy_names,
        'Модель игрушки' : toy_type_names
    })

    # Количество всех игрушек по видам
    df = df.rename(columns={'Наименование игрушки' : 'Количество'})
    df.groupby('Модель игрушки').count().plot(kind='bar').get_figure().savefig('media/images/toy_types.png')

    # Средняя цена игрушек по видам
    df = pd.DataFrame({
        'Наименование игрушки' : toy_names,
        'Модель игрушки' : toy_type_names,
        'Цена' : toy_prices
    })

    df.groupby('Модель игрушки').mean('Цена').plot(kind='bar').get_figure().savefig('media/images/toy_prices.png')

    # Общая информация о цене
    average_price = round(df['Цена'].mean(), 2)
    max_price  = round(df['Цена'].max(), 2)
    min_price = round(df['Цена'].min(), 2)

    # Самая востребованная и невостребованная игрушки
    orders = Order.objects.all()
    order_map = {}
    for order in orders:
        if (order_map.get(order.toy)):
            order_map[order.toy] += order.toy_count
        else:
            order_map[order.toy] = order.toy_count

    popular_toy = max(order_map, key=order_map.get)
    nonpopular_toy = min(order_map, key=order_map.get)

    logging.debug('Статистика продаж создана и сохранена.')

    return render(request, 'statistics/toys_list.html', {'average_price' : average_price,
                                                         'max_price' : max_price,
                                                         'min_price' : min_price, 
                                                         'popular_toy' : popular_toy,
                                                         'popular_toy_count' : order_map[popular_toy],
                                                         'nonpopular_toy' : nonpopular_toy,
                                                         'nonpopular_toy_count' : order_map[nonpopular_toy]})


@permission_required("toyfactory_app.add_employee", login_url='/account/login_employee')
def statistics_profit_view(request):
    # ежемесячный объем продаж игрушек каждого вида
    # годовой отчет поступлений от продаж
    # прогноз продаж
    # построение линейного тренда продаж

    # Годовой отчет поступлений
    orders = Order.objects.all()
    orders_profit = []
    dates = []
    years = []
    count = []
    for order in orders:
        years.append(order.order_date.year)
        dates.append(pd.to_datetime(order.order_date)) 
        orders_profit.append(order.total_price)
        count.append(order.toy_count)

    # Годовой отчет поступлений
    df_year = pd.DataFrame({
        'Года' : years,
        'Прибыль' : orders_profit
    })

    df_year = df_year.groupby('Года').sum()
    df_year.plot(kind='bar').get_figure().savefig('media/images/yearly_profit.png')

    trend_dict = dict(zip(dates, count))
    trend_dict = dict(sorted(trend_dict.items()))
    # Линейный тренд продаж
    df_trend = pd.DataFrame({
        'Даты' : trend_dict.keys(),
        'Продажи' : trend_dict.values()
    })

    plt.clf()
    plt.cla()
    plt.close()
    plt.plot(df_trend['Даты'], df_trend['Продажи'])
    plt.title('Продажи с трендом')
    plt.xlabel('Дата')
    plt.ylabel('Продажи')
    plt.savefig("media/images/trend.png")

    # Прогноз продаж
    df_fr = pd.DataFrame({
        'Даты' : [date for date in dates],
        'Прибыль' : orders_profit
    })

    model = ARIMA(df_fr['Прибыль'], order=(1, 1, 1))
    model_fit = model.fit()

    forecast_future = model_fit.forecast(steps=12)
    future_dates = pd.date_range(start='2024-05-01', periods=12, freq='M')
    forecast_df = pd.DataFrame({'Дата': future_dates, 'Прогноз прибыли': forecast_future})
    df_fr = pd.concat([df_fr, forecast_df], ignore_index=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df_fr.index[:-12], df_fr['Прибыль'][:-12], label='Исходные данные')
    plt.plot(df_fr.index[-12:], df_fr['Прогноз прибыли'][-12:], label='Прогноз')
    plt.title('Прогноз прибыли')
    plt.xlabel('Дата (по месяцам)')
    plt.ylabel('Прибыль')
    plt.legend()
    plt.grid(True)
    plt.savefig("media/images/forecast.png")
    
    logging.debug('Статистика прибыли создана и сохранена.')

    return render(request, 'statistics/profit.html')


@permission_required("toyfactory_app.add_employee", login_url='/account/login_employee')
def statistics_month_view(request):
    toy_types = ToyType.objects.all()
    logging.debug('Статистика по месяцам создана и сохранена.')
    return render(request, 'statistics/month.html', {'toy_types' : toy_types})


@permission_required("toyfactory_app.add_employee", login_url='/account/login_employee')
def statistics_month_detail_view(request, pk=None):
    toy_type = ToyType.objects.all().filter(pk=pk).first()
    toys = Toy.objects.all().filter(toy_type=toy_type)
    orders = Order.objects.all()
    certain_orders = []
    for order in orders:
        if order.toy in toys:
            certain_orders.append(order)

    months = []
    count = []
    for order in certain_orders:
        months.append(order.order_date.month)
        count.append(order.toy_count)

    print(count)

    trend_dict = dict(zip(months, count))
    trend_dict = dict(sorted(trend_dict.items()))
    # Линейный тренд продаж
    df_trend = pd.DataFrame({
        'Месяцы' : trend_dict.keys(),
        'Продажи' : trend_dict.values()
    })

    print(df_trend)

    df_trend = df_trend.groupby('Месяцы').max()
    df_trend.plot(kind='bar').get_figure().savefig('media/images/month_orders.png')
    logging.debug('Месячная статистика создана и сохранена.')

    return render(request, 'statistics/month_detail.html')