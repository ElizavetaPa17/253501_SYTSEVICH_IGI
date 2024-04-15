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


class NewsListView(generic.ListView):
    model = News

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        return context


class NewsDetailView(generic.DetailView):
    model = News


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
    if request.method == 'POST':
        client_form = ClientRegistrationForm(request.POST)
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.save()
            return HttpResponseRedirect(reverse('login_client'))
        else:
            print(client_form.errors)
    
    client_form = ClientRegistrationForm()
    return render(request, 'accounts/register_client.html', {'client_form' : client_form})


def login_client(request):
    error = None
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
    client_form = ClientLoginForm()
    return render(request, 'accounts/login_client.html', {'client_form' : client_form,
                                                          'error' : error})
                

def login_employee(request):
    error = None
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
    employee_form = EmployeeLoginForm()
    return render(request, 'accounts/login_employee.html', {'employee_form' : employee_form, 
                                                            'error' : error})

@login_required
def update_client_profile(request):
    if request.method == "POST":
        client_form = ClientUpdateForm(request.POST, instance=request.user)
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.username = client_form.cleaned_data['username']
            client.save()
            client_group = Group.objects.get(name='Client')
            client_group.user_set.add(client)
            return HttpResponseRedirect(reverse('login_client'))
    client_form = ClientUpdateForm()
    return render(request, 'account/update_client')



@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile_view(request, pk):
    if int(request.user.role) == CLIENT:
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