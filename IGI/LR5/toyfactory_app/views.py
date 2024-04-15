from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .constants import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def news_list_view(request):
    return render(request, 'news/news_list.html')

def toys(request):
    return render(request, 'toys.html')


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


def login_client(request):
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
                

def login_employee(request):
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