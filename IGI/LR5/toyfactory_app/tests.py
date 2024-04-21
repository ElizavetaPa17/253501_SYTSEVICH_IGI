from django.test import TestCase
from django.db.utils import IntegrityError
import datetime
from toyfactory_app.constants import *
from toyfactory_app.models import  *
from django.db import transaction

# Create your tests here.

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
