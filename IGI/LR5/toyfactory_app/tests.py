from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from toyfactory_app.constants import *
from toyfactory_app.models import  *
from toyfactory_app.forms import *

import datetime

# Тесты к моделям
class EmployeeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())

    def tearDown(sulf):
        pass
        
    def test_fields_correctness(self):
        client = Client.object.get(pk=1)
        self.assertEquals(client.first_name, 'Петя')
        self.assertEquals(client.last_name, 'Васечкин')
        self.assertEquals(client.email, 'petyavasechkin@email.com')
        self.assertEquals(client.phone, '+375 (44) 781-54-32')
        self.assertEquals(client.town, 'Минск')
        self.assertEquals(client.address, 'ул. Якуба Коласа')
        self.assertEquals(client.is_active, True)
        self.assertEquals(client.is_staff, False)
        self.assertEquals(client.role, CLIENT)

    def test_uniquness_fields(self):
        try: 
            with transaction.atomic():
                Client.objects.create(first_name="Вася",
                                      last_name='Печкин',
                                      email='petyavasechkin@email.com',
                                      phone='+375 (44) 332-64-12',
                                      town='Минск',
                                      address='ул. Якуба Коласа',
                                      birthday=datetime.datetime.today())
            self.fail('Ошибка дублирования почты')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                Client.objects.create(first_name="Петя",
                                    last_name='Васечкин',
                                    email='someemail@email.com',
                                    phone='+375 (29) 312-34-12',
                                    town='Минск',
                                    address='ул. Якуба Коласа',
                                    birthday=datetime.datetime.today())
            self.fail('Ошибка дублирования имени и фамилии')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                Client.objects.create(first_name="Глеб",
                                    last_name='Сморчков',
                                    email='gleb@email.com',
                                    phone='+375 (44) 781-54-32',
                                    town='Минск',
                                    address='ул. Якуба Коласа',
                                    birthday=datetime.datetime.today())
            self.fail('Ошибка дублирования номера')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                Client.objects.create(first_name="Вася",
                                    last_name='Сморчков',
                                    email='koko@email.com',
                                    phone='+375 (29) 512-34-12',
                                    town='Минск',
                                    address='ул. Якуба Коласа',
                                    birthday=datetime.datetime.today())
        except IntegrityError:
            self.fail('Проверка на уникальность имени и фаамилии ошибочна')


    def test_phone_format(self):
        try:
            with transaction.atomic():
                Client.objects.create(first_name="Лиля",
                                    last_name='Трубочкина',
                                    email='lilya@email.com',
                                    phone='+375 44 781-54-32',
                                    town='Минск',
                                    address='ул. Якуба Коласа',
                                    birthday=datetime.datetime.today())
            self.fail('Некорректный формат номера')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                Client.objects.create(first_name="Лиля",
                                    last_name='Трубочкина',
                                    email='lilya@email.com',
                                    phone='+375 (44) 781 54 32',
                                    town='Минск',
                                    address='ул. Якуба Коласа',
                                    birthday=datetime.datetime.today())
            self.fail('Некорректный формат номера')
        except IntegrityError:
            pass
                
    def test_url(self):
        self.assertEquals(Client.object.get(pk=1).get_absolute_url(), "account/account_details")


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())

    def tearDown(sulf):
        pass

    def test_role_corectness(self):
        self.assertEquals(Employee.objects.all().filter(pk=1).first().role, EMPLOYEE)

    
class CompanyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Company.objects.create(name='Фабрика игрушек',
                               address='Минск, ул. Якуба Коласа',
                               email='toyfactory@email.com',
                               creation=datetime.datetime.today())
    
    def test_fields_correctness(self):
        self.assertEquals(Company.objects.get(pk=1).name, 'Фабрика игрушек')
        self.assertEquals(Company.objects.get(pk=1).address, 'Минск, ул. Якуба Коласа')
        self.assertEquals(Company.objects.get(pk=1).email, 'toyfactory@email.com')


class NewsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        News.objects.create(title='Новое поступление игрушек!',
                            description='Новые игрушки!')
    
    def test_fields_correctness(self):
        self.assertEquals(News.objects.get(pk=1).title, 'Новое поступление игрушек!')
        self.assertEquals(News.objects.get(pk=1).description, 'Новые игрушки!')

    def test_title_uniqueness(self):
        try:
            with transaction.atomic():
                News.objects.create(title='Новое поступление игрушек!',
                                    description='Пора закупаться!')
            self.fail('Ошибка уникальности заголовка новостей')
        except IntegrityError:
            pass

    def test_get_absolute_url(self):
        self.assertEquals(News.objects.get(pk=1).get_absolute_url(), '/news/detail/1')


class TermsDictionaryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TermsDictionary.objects.create(question='Как сделать заказ?',
                                       answer='Просто так!',
                                       date=datetime.date.today())

    def test_fields_correctness(self):
        self.assertEquals(TermsDictionary.objects.get(pk=1).question, 'Как сделать заказ?')
        self.assertEquals(TermsDictionary.objects.get(pk=1).answer, 'Просто так!')

    def test_question_uniqueness(self):
        try:
            with transaction.atomic():
                TermsDictionary.objects.create(question='Как сделать заказ?',
                                               answer='Какой заказ?')
            self.fail('Ошибка заголовка вопроса')
        except IntegrityError:
            pass


class VacationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Vacation.objects.create(position='Первый секретарь',
                                description='Нужен первый секретарь')

    def test_fields_correctness(self):
        self.assertEquals(Vacation.objects.get(pk=1).position, 'Первый секретарь')
        self.assertEquals(Vacation.objects.get(pk=1).description, 'Нужен первый секретарь')

    def test_position_uniqueness(self):
        try:
            with transaction.atomic():
                Vacation.objects.create(position='Первый секретарь',
                                        description='Срочно нужен секретарь')
            self.fail('Ошибка уникальности занимаемой должности')
        except IntegrityError:
            pass


class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())

        Client.objects.create(first_name="Вася",
                              last_name='Печкин',
                              email='vasya@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())

        Feedback.objects.create(user=Client.objects.get(pk=1), 
                                title='Хорошая продукция!',
                                mark=4,
                                description='Очень хорошая продукция!',
                                date=datetime.datetime.today())

    def test_fields_correctness(self):
        self.assertEquals(Feedback.objects.get(pk=1).user, Client.objects.get(pk=1))
        self.assertEquals(Feedback.objects.get(pk=1).title, 'Хорошая продукция!')
        self.assertEquals(Feedback.objects.get(pk=1).mark, 4)
        self.assertEquals(Feedback.objects.get(pk=1).description, 'Очень хорошая продукция!')

    def test_field_uniqueness(self):
        try:
            with transaction.atomic():
                Feedback.objects.create(user=Client.objects.get(pk=1),
                                        title='Отличная продукция!',
                                        mark=5,
                                        description='Очень хорошая продукция!',
                                        date=datetime.datetime.today())
            self.fail('Ошибка уникальности автора запроса')
        except IntegrityError:
            pass


class ToyTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ToyType.objects.create(name='Машины',
                               slug='cars')


    def test_fields_correctness(self):
        self.assertEquals(ToyType.objects.get(pk=1).name, 'Машины')
        self.assertEquals(ToyType.objects.get(pk=1).slug, 'cars')


    def test_fields_uniqueness(self):
        try:
            with transaction.atomic():
                ToyType.objects.create(name='Машины',
                                       slug='cars')
            self.fail('Ошибка уникальности имени модели игрушки')
        except IntegrityError:
            pass

    def test_get_absolute_url(self):
        self.assertEquals(ToyType.objects.get(pk=1).get_absolute_url(), '/toy/list/cars')


class ToyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ToyType.objects.create(name='Машины',
                               slug='cars')
        Toy.objects.create(name='УАЗ Патриот',
                           price=100,
                           toy_type=ToyType.objects.get(pk=1),
                           produced=True)
    
    def test_fields_correctness(self):
        self.assertEquals(Toy.objects.get(pk=1).name, 'УАЗ Патриот')
        self.assertEquals(Toy.objects.get(pk=1).price, 100)
        self.assertEquals(Toy.objects.get(pk=1).toy_type, ToyType.objects.get(pk=1))
        self.assertEquals(Toy.objects.get(pk=1).produced, True)


    def test_fields_uniqueness(self):
        try:
            with transaction.atomic():
                Toy.objects.create(name='УАЗ Патриот',
                                   price=110,
                                   toy_type=ToyType.objects.get(pk=1),
                                   produced=False)
            self.fail('Ошибка уникальности имени игрушки')
        except IntegrityError:
            pass

    def test_get_absolute_url(self):
        self.assertEquals(Toy.objects.get(pk=1).get_absolute_url(), '/toy/detail/1')

class PromocodeTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PromocodeType.objects.create(name='Активный',
                                     slug='active')

    def test_fields_correctness(self):
        self.assertEquals(PromocodeType.objects.get(pk=1).name, 'Активный')
        self.assertEquals(PromocodeType.objects.get(pk=1).slug, 'active')
    
    def test_fields_uniqueness(self):
        try:
            with transaction.atomic():
                PromocodeType.objects.create(name='Активный',
                                             slug='new_discount')
            self.fail('Ошибка уникальности имени вида промокода')
        except IntegrityError:
            pass

    def test_get_absolute_url(self):
        self.assertEquals(PromocodeType.objects.get(pk=1).get_absolute_url(), '/promocodes/list/active')


class PromocodeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PromocodeType.objects.create(name='Активный',
                                     slug='active')

        PromocodeType.objects.create(name='Неактивный',
                                     slug='unactive')

        Promocode.objects.create(name='Скидки именниникам',
                                 discount=50, 
                                 promocode_type=PromocodeType.objects.get(pk=1))

    
    def test_fields_correctness(self):
        self.assertEquals(Promocode.objects.get(pk=1).name, 'Скидки именниникам')
        self.assertEquals(Promocode.objects.get(pk=1).discount, 50)
        self.assertEquals(Promocode.objects.get(pk=1).promocode_type, PromocodeType.objects.get(pk=1))


    def test_field_uniqueness(self):
        try:
            with transaction.atomic():
                Promocode.objects.create(name='Скидки именниникам',
                                 discount=40, 
                                 promocode_type=PromocodeType.objects.get(pk=2))
            self.fail('Ошибка уникальности имени промокода')
        except IntegrityError:
            pass

    pass

class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())

        ToyType.objects.create(name='Машины',
                               slug='cars')

        Toy.objects.create(name='УАЗ Патриот',
                           price=100,
                           toy_type=ToyType.objects.get(pk=1),
                           produced=True)

        PromocodeType.objects.create(name='Активный',
                                     slug='active')

        Promocode.objects.create(name='Скидки именниникам',
                                 discount=50, 
                                 promocode_type=PromocodeType.objects.get(pk=1))

        Order.objects.create(order_date=datetime.datetime.today(),
                             finish_date=datetime.datetime.today(),
                             client=Client.objects.get(pk=1),
                             toy=Toy.objects.get(pk=1),
                             toy_count=10,
                             total_price=10*Toy.objects.get(pk=1).price,
                             promocodes=Promocode.objects.get(pk=1))


    def test_fields_correctness(self):
        self.assertEquals(Order.objects.get(pk=1).client, Client.objects.get(pk=1))
        self.assertEquals(Order.objects.get(pk=1).toy, Toy.objects.get(pk=1))
        self.assertEquals(Order.objects.get(pk=1).toy_count, 10)
        self.assertEquals(Order.objects.get(pk=1).total_price, 10*Toy.objects.get(pk=1).price)
        self.assertEquals(Order.objects.get(pk=1).promocodes, Promocode.objects.get(pk=1))


# Тесты к формам
class TestClientRegistrationForm(TestCase):
    def test_form_labels(self):
        form = ClientRegistrationForm()
        self.assertEquals(form.fields['phone'].label, 'Телефон')
        self.assertEquals(form.fields['town'].label, 'Город')
        self.assertEquals(form.fields['address'].label, 'Адрес')
        self.assertEquals(form.fields['first_name'].label, 'Имя')
        self.assertEquals(form.fields['last_name'].label, 'Фамилия')
        self.assertEquals(form.fields['email'].label, 'Почта')
        self.assertEquals(form.fields['password1'].label, 'Пароль')
        self.assertEquals(form.fields['password2'].label, 'Подтверждение пароля')

    def test_form_phone_format(self):
        form = ClientRegistrationForm({ 'first_name' : 'Паша',
                                        'last_name'  : 'Григоренко',
                                        'email'      : "pasha@email.com",
                                        'phone'      : '375 (44) 431-21-21',
                                        'town'       : 'Minsk',
                                        'address'    : 'ул. Якуба Коласа',
                                        'birthday'    : datetime.date(year=2001, day=21, month=2),
                                        'password1'  : "bzjswkw312dmwdwd",
                                        'password2'  : 'bzjswkw312dmwdwd'})
        self.assertFalse(form.is_valid())

    def test_form_birthay(self):
        form = ClientRegistrationForm({ 'first_name' : 'Паша',
                                        'last_name'  : 'Григоренко',
                                        'email'      : "pasha@email.com",
                                        'phone'      : '+375 (44) 431-21-21',
                                        'town'       : 'Minsk',
                                        'address'    : 'ул. Якуба Коласа',
                                        'birthday'   :  datetime.date.today(),
                                        'password1'  : "123",
                                        'password2'  : '123'})
        self.assertFalse(form.is_valid())

    def test_form_passwords(self):
        form = ClientRegistrationForm({ 'first_name' : 'Паша',
                                        'last_name'  : 'Григоренко',
                                        'email'      : "pasha@email.com",
                                        'phone'      : '+375 (44) 431 21-21',
                                        'town'       : 'Minsk',
                                        'address'    : 'ул. Якуба Коласа',
                                        'birthday'    :  datetime.date(year=2001, day=21, month=2),
                                        'password1'  : "091",
                                        'password2'  : '123'})
        self.assertFalse(form.is_valid())

    def test_form_fields_uniqueness(self):
        Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.date(year=2001, month=2, day=1))

        form = ClientRegistrationForm({ 'first_name' : 'Петя',
                                        'last_name'  : 'Васечкин',
                                        'email'      : "pasha@email.com",
                                        'phone'      : '+375 (44) 431 21-21',
                                        'town'       : 'Minsk',
                                        'address'    : 'ул. Якуба Коласа',
                                        'birthday'    :  datetime.date(year=2001, day=21, month=2),
                                        'password1'  : "123",
                                        'password2'  : '123'})
        self.assertFalse(form.is_valid())

        form = ClientRegistrationForm({ 'first_name' : 'Маша',
                                        'last_name'  : 'Мартынова',
                                        'email'      : "petyavasechkin@email.com",
                                        'phone'      : '+375 (44) 431 21-21',
                                        'town'       : 'Minsk',
                                        'address'    : 'ул. Якуба Коласа',
                                        'birthday'    :  datetime.date(year=2001, day=21, month=2),
                                        'password1'  : "123",
                                        'password2'  : '123'})
        self.assertFalse(form.is_valid())

        form = ClientRegistrationForm({ 'first_name' : 'Маша',
                                        'last_name'  : 'Мартынова',
                                        'email'      : "masha@email.com",
                                        'phone'      : '+375 (44) 781-54-32',
                                        'town'       : 'Minsk',
                                        'address'    : 'ул. Якуба Коласа',
                                        'birthday'    :  datetime.date(year=2001, day=21, month=2),
                                        'password1'  : "123",
                                        'password2'  : '123'})
        self.assertFalse(form.is_valid())

class TestClientLoginForm(TestCase):
    def test_form_labels(self):
        form = ClientLoginForm()
        self.assertEquals(form.fields['first_name'].label, 'Имя')
        self.assertEquals(form.fields['last_name'].label, 'Фамилия')
        self.assertEquals(form.fields['password1'].label, 'Пароль')


class TestProfileUpdateForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        form = ClientRegistrationForm({ 'first_name' : 'Петя',
                                 'last_name'  : 'Васечкин',
                                 'email'      : "pasha@email.com",
                                 'phone'      : '+375 (44) 431-21-21',
                                 'town'       : 'Minsk',
                                 'address'    : 'ул. Якуба Коласа',
                                 'birthday'    :  datetime.date(year=2001, day=21, month=2),
                                 'password1'  : "12dewkmd2390ek",
                                 'password2'  : '12dewkmd2390ek'})

        form.save()

    def test_form_labels(self):
        form = ProfileUpdateForm()
        self.assertEquals(form.fields['phone'].label, 'Телефон')
        self.assertEquals(form.fields['town'].label, 'Город')
        self.assertEquals(form.fields['address'].label, 'Адрес')
        self.assertEquals(form.fields['image'].label, 'Фото')
        self.assertEquals(form.fields['password1'].label, 'Пароль')
        self.assertEquals(form.fields['password2'].label, 'Подтверждение пароля')

    def test_form_phone_format(self):
        form = ProfileUpdateForm({ 'phone'      : '+375 (44) 31-21-21',
                                   'town'       : 'Minsk',
                                   'address'    : 'ул. Якуба Коласа',
                                   'password1'  : "bzjswkw312dmwdwd",
                                   'password2'  : 'bzjswkw312dmwdwd'},
                                   instance=Client.objects.get(pk=1))
        self.assertFalse(form.is_valid())

        form = ProfileUpdateForm({ 'phone'      : '+375 (44) 421-21-21',
                                   'town'       : 'Minsk',
                                   'address'    : 'ул. Якуба Коласа',
                                   'password1'  : "bzjswkw312dmwdwd",
                                   'password2'  : 'bzjswkw312dmwdwd',
                                   'instance'   : Client.objects.get(pk=1)})
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_form_passwords(self):
        form = ProfileUpdateForm({ 'phone'      : '+375 (44) 31-21-21',
                                   'town'       : 'Minsk',
                                   'address'    : 'ул. Якуба Коласа',
                                   'password1'  : "bzjswkw312dqwok",
                                   'password2'  : 'bzjswkw312dmwdwd'},
                                   instance=Client.objects.get(pk=1))
        self.assertFalse(form.is_valid())


class TestEmployeeLoginForm(TestCase):
    def test_form_labels(self):
        form = EmployeeLoginForm()
        self.assertEquals(form.fields['first_name'].label, 'Имя')
        self.assertEquals(form.fields['last_name'].label, 'Фамилия')
        self.assertEquals(form.fields['password1'].label, 'Пароль')

class TestFeedbackForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        form = ClientRegistrationForm({ 'first_name' : 'Петя',
                                 'last_name'  : 'Васечкин',
                                 'email'      : "pasha@email.com",
                                 'phone'      : '+375 (44) 431-21-21',
                                 'town'       : 'Minsk',
                                 'address'    : 'ул. Якуба Коласа',
                                 'birthday'    :  datetime.date(year=2001, day=21, month=2),
                                 'password1'  : "12dewkmd2390ek",
                                 'password2'  : '12dewkmd2390ek'})

        form.is_valid()
        form.save()

    def test_form_labels(self):
        form = FeedbackForm()
        self.assertEquals(form.fields['title'].label, 'Заголовок')
        self.assertEquals(form.fields['mark'].label, 'Оценка')
        self.assertEquals(form.fields['description'].label, 'Описание')

    def test_mark_corectness(self):
        form = FeedbackForm({'title' : 'Интересная фабрика!',
                             'mark' : 4,
                             'description' : 'Спасибо!'})
        self.assertTrue(form.is_valid())

        form = FeedbackForm({'title' : 'Интересная фабрика!',
                             'mark' : -1,
                             'description' : 'Спасибо!'})
        self.assertFalse(form.is_valid())

        form = FeedbackForm({'title' : 'Интересная фабрика!',
                             'mark' : 7,
                             'description' : 'Спасибо!'})
        
        self.assertFalse(form.is_valid())

    def test_title_uniqueness(self):
        form = FeedbackForm({'title' : 'Интересная фабрика!',
                             'mark' : 4,
                             'description' : 'Спасибо!'})
        feedback_form = form.save(commit=False)
        feedback_form = Client.objects.get(pk=1)
        feedback_form.date = datetime.date.today()
        
        feedback_form.save()


# Тестирование отображений
class AddFeedbackTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.user_permissions.add(Permission.objects.get(codename='add_feedback'))
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('add_feedback'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_client'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('add_feedback'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_client'))

    def test_redirect_if_logged_in_with_correct_permission(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('add_feedback'))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('add_feedback'))

        self.assertTemplateUsed(resp, 'feedbacks/form.html')

class AboutEmployeesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employees_list'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_client'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('employees_list'))

        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('employees_list'))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('employees_list'))

        self.assertTemplateUsed(resp, 'toyfactory_app/employee_list.html')


class EmployeeDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employee_detail', kwargs={"pk" : 2}))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_client'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('employee_detail', kwargs={"pk" : 2}))

        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('employee_detail', kwargs={"pk" : 2}))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('employee_detail', kwargs={"pk" : 2}))

        self.assertTemplateUsed(resp, 'toyfactory_app/employee_detail.html')

class UpdateProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('update_profile', kwargs={"pk" : 1}))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_client'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('update_profile', kwargs={"pk" : 1}))

        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('update_profile', kwargs={"pk" : 2}))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('update_profile', kwargs={"pk" : 1}))

        self.assertTemplateUsed(resp, 'accounts/update_profile.html')


class LogoutTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('logout'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_client'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('logout'))

        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('logout'))

        self.assertEqual(resp.status_code, 302)


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.user_permissions.add(Permission.objects.get(codename='add_order'))
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('profile', kwargs={"pk" : 1}))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_client'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('profile', kwargs={"pk" : 1}))

        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('profile', kwargs={"pk" : 2}))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('profile', kwargs={"pk" : 2}))

        self.assertTemplateUsed(resp, 'accounts/profile.html')


class CreateOrderView(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.user_permissions.add(Permission.objects.get(codename='add_order'))
        client.set_password('123')
        client.save()

        ToyType.objects.create(name='Машины',
                               slug='car')

        Toy.objects.create(name='Москвич',
                           price=300,
                           toy_type=ToyType.objects.get(pk=1),
                           produced=True)


    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('create_order', kwargs={"pk" : 1}))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_client'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('create_order', kwargs={"pk" : 1}))

        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('create_order', kwargs={"pk" : 1}))

        self.assertEqual(resp.status_code, 302)

    def test_uses_correct_template(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('create_order', kwargs={"pk" : 1}))

        self.assertTemplateUsed(resp, 'toy/create_order.html')


class EmployeeClientsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.user_permissions.add(Permission.objects.get(codename='view_client'))
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('employee_clients_list'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('employee_clients_list'))

        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('employee_clients_list'))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('employee_clients_list'))

        self.assertTemplateUsed(resp, 'clients/my_clients.html')


class ClientOrdersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.user_permissions.add(Permission.objects.get(codename='view_order'))
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('client_orders_list', kwargs={"pk" : 1}))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('client_orders_list', kwargs={"pk" : 1}))

        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('client_orders_list', kwargs={"pk" : 1}))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('client_orders_list', kwargs={"pk" : 1}))

        self.assertTemplateUsed(resp, 'clients/client_orders.html')


class MyOrdersView(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.user_permissions.add(Permission.objects.get(codename='view_order'))
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my_orders_list'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_client'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('my_orders_list'))

        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('my_orders_list'))

        self.assertEqual(resp.status_code, 302)

    def test_uses_correct_template(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('my_orders_list'))

        self.assertTemplateUsed(resp, 'clients/my_orders.html')


class StatisticsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        employee = User.objects.create_superuser(email='admin@email.com',
                                                password='123')

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('statistics'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('statistics'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('statistics'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_admin(self):
        login = self.client.login(email='admin@email.com', password='123')
        resp = self.client.get(reverse('statistics'))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(email='admin@email.com', password='123')
        resp = self.client.get(reverse('statistics'))

        self.assertTemplateUsed(resp, 'statistics/index.html')


class StatisticsPriceViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        employee = User.objects.create_superuser(email='admin@email.com',
                                                password='123')

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('statistics_price_list'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('statistics_price_list'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('statistics_price_list'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_admin(self):
        login = self.client.login(email='admin@email.com', password='123')
        resp = self.client.get(reverse('statistics_price_list'))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(email='admin@email.com', password='123')
        resp = self.client.get(reverse('statistics_price_list'))

        self.assertTemplateUsed(resp, 'statistics/price_list.html')

    
class StatisticsClientsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        employee = User.objects.create_superuser(email='admin@email.com',
                                                password='123')

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('statistics_clients'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('statistics_clients'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('statistics_clients'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_admin(self):
        login = self.client.login(email='admin@email.com', password='123')
        resp = self.client.get(reverse('statistics_clients'))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(email='admin@email.com', password='123')
        resp = self.client.get(reverse('statistics_clients'))

        self.assertTemplateUsed(resp, 'statistics/clients_town_list.html')


class StatisticsToyViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        employee = User.objects.create_superuser(email='admin@email.com',
                                                password='123')

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('statistics_toys'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('statistics_toys'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('statistics_toys'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

class StatisticsProfitViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        employee = User.objects.create_superuser(email='admin@email.com',
                                                password='123')

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('statistics_profit'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('statistics_profit'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('statistics_profit'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

class StatisticsMonthViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        employee = User.objects.create_superuser(email='admin@email.com',
                                                password='123')

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('statistics_month'))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('statistics_month'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('statistics_month'))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_admin(self):
        login = self.client.login(email='admin@email.com', password='123')
        resp = self.client.get(reverse('statistics_month'))

        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(email='admin@email.com', password='123')
        resp = self.client.get(reverse('statistics_month'))

        self.assertTemplateUsed(resp, 'statistics/month.html')


class StatisticsMonthDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        employee = Employee.objects.create(first_name="Томас",
                              last_name='Петров',
                              email='tomes@email.com',
                              phone='+375 (29) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        employee.set_password('123')
        employee.save()

        employee = User.objects.create_superuser(email='admin@email.com',
                                                 password='123')

        client = Client.objects.create(first_name="Петя",
                              last_name='Васечкин',
                              email='petyavasechkin@email.com',
                              phone='+375 (44) 781-54-32',
                              town='Минск',
                              address='ул. Якуба Коласа',
                              birthday=datetime.datetime.today())
        client.set_password('123')
        client.save()

        ToyType.objects.create(name='Машины',
                               slug='car')

        Toy.objects.create(name='Москвич',
                           price=300,
                           toy_type=ToyType.objects.get(pk=1),
                           produced=True)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('statistics_month_detail', kwargs={"pk" : 1}))

        self.assertEquals(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_client(self):
        login = self.client.login(first_name='Петя', last_name='Васечкин', password='123')
        resp = self.client.get(reverse('statistics_month_detail', kwargs={"pk" : 1}))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))

    def test_redirect_if_logged_in_as_employee(self):
        login = self.client.login(first_name='Томас', last_name='Петров', password='123')
        resp = self.client.get(reverse('statistics_month_detail', kwargs={"pk" : 1}))

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/login_employee'))


class IndexTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('index'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')


class NewsListViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('news_list'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'news/list.html')


class NewsDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        News.objects.create(title='Новое поступление!',
                            image='../media/images/no_photo.png',
                            description='Новые игрушки')

    def test_redirect(self):
        resp = self.client.get(reverse('news_detail', kwargs={'pk':1}))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'news/detail.html')


class PromocodesViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('promocodes_list'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'promocodes.html')


class FeedbackViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('feedbacks'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'feedbacks/list.html')

    
class PolicyViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('policy'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'policy.html')


class VacationsViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('vacations'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'vacations.html')


class AboutViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('about'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'about.html')


class TerminesViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('termines'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'termines.html')


class RegisterClientViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('register_client'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/register_client.html')


class LoginClientViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('login_client'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/login_client.html')


class LoginEmployeeViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('login_employee'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'accounts/login_employee.html')


class ToyListViewTest(TestCase):
    def test_redirect(self):
        resp = self.client.get(reverse('toys_list'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'toy/list.html')


class ToyListByTypeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ToyType.objects.create(name='Машины',
                               slug='car')

        Toy.objects.create(name='Москвич',
                           price=300,
                           toy_type=ToyType.objects.get(pk=1),
                           produced=True)

    def test_redirect(self):
        resp = self.client.get(reverse('toys_list'))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'toy/list.html')


class ToyDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ToyType.objects.create(name='Машины',
                               slug='car')

        Toy.objects.create(name='Москвич',
                           price=300,
                           toy_type=ToyType.objects.get(pk=1),
                           produced=True)

    def test_redirect(self):
        resp = self.client.get(reverse('toy_detail', kwargs={'pk':1}))

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'toy/detail.html')