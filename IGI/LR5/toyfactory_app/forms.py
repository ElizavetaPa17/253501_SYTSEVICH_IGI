from django import forms
from .models import Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ClientRegistrationForm(UserCreationForm):
    phone = forms.CharField(label='Телефон', widget=forms.TextInput)
    town = forms.CharField(label='Город', widget=forms.TextInput)
    address = forms.CharField(label='Адрес', widget=forms.TextInput)

    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput()
    )

    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput()
    )

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'town', 'address', 'password1', 'password2')

    def clean_password2(self):
        clean_data = self.cleaned_data
        if clean_data['password1'] != clean_data['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return clean_data['password2']


class ClientLoginForm(forms.Form):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput()
    )

    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput()
    )

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password1')
        

class EmployeeLoginForm(forms.Form):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput()
    )

    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput()
    )

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password1')