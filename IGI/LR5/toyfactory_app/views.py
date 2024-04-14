from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')


class NewsListView(generic.ListView):
    model = News

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        return context


class NewsDetailView(generic.DetailView):
    model = News


def toys(request):
    return render(request, 'toys.html')


class EmployeeListView(generic.ListView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        return context


class EmployeeDetailView(generic.DetailView):
    model = Employee


def promocodes(request):
    return render(request, 'promocodes.html')


def feedbacks(request):
    return render(request, 'feedbacks.html')


def policy(request):
    return render(request, 'policy.html')


def vacations(request):
    return render(request, 'vacations.html')


def about(request):
    return render(request, 'about.html')


def termines(request):
    return render(request, 'termines.html')


def register_client(request):
    if request.method == 'POST':
        client_form = ClientRegistrationForm(request.POST)
        if client_form.is_valid():
            client_form.cleaned_data['username'] = client_form.cleaned_data['first_name'] + \
                                                   client_form.cleaned_data['last_name']

            first_name = client_form.cleaned_data['first_name']
            last_name = client_form.cleaned_data['last_name']
            email = client_form.cleaned_data['email']

            try:
                user = User.objects.get(email=email, first_name=first_name, last_name=last_name)
                if Client.objects.filter(user=user):
                    messages.error('Пользователь с такими данными уже существует.')
                else:
                    client = client_form.save(commit=False)
                    client.username = client_form.cleaned_data['username']
                    client.save()
                    client_group = Group.objects.get(name='Client')
                    client_group.user_set.add(client)
                    return HttpResponseRedirect(reverse('login_client'))
            except:
                client = client_form.save(commit=False)
                client.username = client_form.cleaned_data['username']
                client.save()
                client_group = Group.objects.get(name='Client')
                client_group.user_set.add(client)
                return HttpResponseRedirect(reverse('login_client'))
        else:
            messages.error(request, 'Невалидные данные в форме.')
    
    messages.error(request, 'Ошибка регистрации.')
    client_form = ClientRegistrationForm()
    return render(request, 'accounts/register_client.html', {'client_form' : client_form})


def login_client(request):
    if request.method == 'POST':
        client_form = ClientLoginForm(request.POST)
        if client_form.is_valid():
            first_name = client_form.cleaned_data.get('first_name')
            last_name = client_form.cleaned_data.get('last_name')
            password = client_form.cleaned_data.get('password1')
            user = authenticate(username=first_name+last_name,
                                first_name=first_name, 
                                last_name=last_name,
                                password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                print(first_name+last_name)
                messages.error(request, 'Клиент с такими данными не найден.')
    client_form = ClientLoginForm()
    return render(request, 'accounts/login_client.html', {'client_form' : client_form})
                

def login_employee(request):
    if request.method == 'POST':
        employee_form = EmployeeLoginForm(request.POST)
        if employee_form.is_valid():
            first_name = employee_form.cleaned_data.get('first_name')
            last_name = employee_form.cleaned_data.get('last_name')
            password = employee_form.cleaned_data.get('password1')
            employee = authenticate(username=first_name+last_name,
                                    first_name=first_name,
                                    last_name=last_name, 
                                    password=password)
            if employee:
                login(request, employee)
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, 'Сотрудник с такими данными не найден.')
    employee_form = EmployeeLoginForm()
    return render(request, 'accounts/login_employee.html', {'employee_form' : employee_form})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile_view(request, pk):
    if request.user.has_perm('client.add_order'):
        return render(request, 'accounts/client_profile.html')
    else:
        return render(request, 'accounts/employee_profile.html')


def toys_list(request, toy_type_slug=None):
    toy_type = None
    toys = Toy.objects.all()
    toy_types = ToyType.objects.all()
    if toy_type:
        toy_type = get_object_or_404(ToyType, slug=toy_type_slug)
        toys = toys.filter(toy_type=toy_type)
    return render(request, 'toy/list.html', {'toy_type'  : toy_type, 
                                             'toy_types' : toy_types,
                                             'toys' : toys })


def toy_details(request, id):
    toy = get_object_or_404(Toy, id=id)
    return render(request, 'toy/toy_details.html', { 'toy' : toy })