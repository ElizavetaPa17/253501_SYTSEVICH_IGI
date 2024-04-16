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

# Create your views here.
def index(request):
    news_list = News.objects.all()
    news = None
    if news_list:
        news = news_list[0]
    return render(request, 'index.html', {'news' : news})

def news_list_view(request):
    news_list = News.objects.all()
    return render(request, 'news/list.html', {'news_list' : news_list})


def news_detail_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/detail.html', {'news' : news})


def promocodes(request):
    return render(request, 'promocodes.html')


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


def add_feedback_view(request):
    errors = None
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
        else:
            errors = feedback_form.errors
    feedback_form = FeedbackForm()
    return render(request, 'feedbacks/form.html', {'feedback_form' : feedback_form, 
                                                   'errors' : errors})


def policy(request):
    return render(request, 'policy.html')


def vacations(request):
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


def about(request):
    company = Company.objects.all()
    company = company[0]
    return render(request, 'about.html', {'company' : company})


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


def toys_list(request, toy_type=None):
    ttype = None
    toys = Toy.objects.all()
    toy_types=None
    toy_types = ToyType.objects.all()
    if toy_type:
        ttype = get_object_or_404(ToyType, slug=toy_type)
        toys = toys.filter(toy_type=ttype)
    return render(request, 'toy/list.html', {'ttype'  : ttype, 
                                             'ttypes' : toy_types,
                                             'toys' : toys })


def toy_details(request, pk):
    toy = get_object_or_404(Toy, pk=pk)
    return render(request, 'toy/detail.html', { 'toy' : toy ,
                                                'required_role' : CLIENT})