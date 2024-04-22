from django import forms
#from .models import Client
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
import re
from datetime import date
from .models import *

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

    email = forms.CharField(
        label='Почта',
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
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone', 'town', 'address', 'birthday', 'password1', 'password2')

    def clean_password2(self):
        clean_data = self.cleaned_data
        if clean_data['password1'] != clean_data['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return clean_data['password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone and not re.match(r"^\+375\s{1}\([\d]{2}\)\s{1}[\d]{3}-[\d]{2}-[\d]{2}$", phone):
            raise forms.ValidationError('Некорректный формат номера')
        elif phone and Client.objects.filter(phone=phone).count():
            raise forms.ValidationError("Данный номер уже в использовании.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError("Данная почта уже в использовании.")
        return email

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        today = date.today()
        if birthday and (today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))) >= 18:
            return birthday
        else:
            raise forms.ValidationError("Вы должны быть старше 18 лет.")

    def clean_username(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if last_name and first_name and User.objects.filter(first_name=first_name,
                                                            last_name=last_name):
            raise forms.ValidationError("Данное ФИО уже в использовании.")
        return first_name+last_name
        

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
        model = Client
        fields = ('first_name', 'last_name', 'password1')


class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(label='Телефон', widget=forms.TextInput)
    town = forms.CharField(label='Город', widget=forms.TextInput)
    address = forms.CharField(label='Адрес', widget=forms.TextInput)

    image = forms.ImageField(label='Фото', required=False)

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
        fields = ('phone', 'town', 'address', 'image', 'password1', 'password2')

    def clean_password2(self):
        clean_data = self.cleaned_data
        if clean_data['password1'] != clean_data['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return clean_data['password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone and not re.match(r"^\+375\s{1}\([\d]{2}\)\s{1}[\d]{3}-[\d]{2}-[\d]{2}$", phone):
            raise forms.ValidationError('Некорректный формат номера')
        return phone


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
        model = Employee
        fields = ('first_name', 'last_name', 'password1')


class FeedbackForm(forms.ModelForm):
    title = forms.CharField(max_length=150, label='Заголовок')   
    mark = forms.IntegerField(label='Оценка',
                              validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), label='Описание')

    class Meta:
        model = Feedback
        fields = ('title', 'mark', 'description')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('toy_count', 'promocodes')