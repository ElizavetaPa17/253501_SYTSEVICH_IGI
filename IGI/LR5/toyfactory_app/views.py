from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from .constants import *
import pandas as pd
import datetime
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def index(request):
    news_list = News.objects.all()
    news = None
    if news_list:
        news = news_list[0]

    #users = User.objects.all()
    #for user in users:
    #    user.set_password('bz718nqf45')
    ##    print(user.password)
    #    user.save()
    
    return render(request, 'index.html', {'news' : news})

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


@login_required
def add_feedback_view(request):
    errors = None
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.user = request.user
            feedback.date = datetime.date.today()
            feedback.save()
        else:
            errors = feedback_form.errors
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
    company = Company.objects.all()
    company = company[0]
    return render(request, 'about.html', {'company' : company})


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
            return HttpResponseRedirect(reverse('login_client'))
        else:
            errors = client_form.errors
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
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                error = 'Клиент с такими данными не найден.'
        else:
            errors = client_form.errors
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
            if employee:
                login(request, employee)
                print('here')
                return HttpResponseRedirect(reverse('index'))
            else:
                error = 'Сотрудник с такими данными не найден.'
        else:
            errors = employee_form.errors
    employee_form = EmployeeLoginForm()
    return render(request, 'accounts/login_employee.html', {'employee_form' : employee_form,
                                                            'errors' : errors, 
                                                            'error' : error})

@login_required
def update_profile_view(request, pk):
    errors = None
    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('login_client'))
        else:
            errors = profile_form.errors
    profile_form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/update_profile.html', {'profile_form' :  profile_form,
                                                            'errors' : errors})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
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
            order.total_price = order.toy.price * order_form.cleaned_data['toy_count'] * (1 - order_form.cleaned_data['promocodes'][0].discount / 100)
            order.save()

            return HttpResponseRedirect(reverse('toys_list'))
        else:
            errors = order_form.errors
    order_form = OrderForm()
    return render(request, 'toy/create_order.html', {'order_form' :  order_form,
                                                     'errors' : errors})

    pass


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


@login_required
def statistics_view(request):
    return render(request, 'statistics/index.html')


@login_required
def statistics_price_view(request):
    toys = Toy.objects.all()
    return render(request, 'statistics/price_list.html', {'toys' : toys})


def clients_town_view(request):
    clients = Client.objects.all().order_by('town')
    towns = []
    for client in clients:
        print(client.email)
        towns.append(client.town)

    print(pd.DataFrame(clients))

    paginator = Paginator(clients, 5)
    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)
    return render(request, 'statistics/clients_town_list.html', {
                                                                 'clients' : clients,
                                                                 'page' : page })