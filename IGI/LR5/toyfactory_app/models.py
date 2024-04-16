from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .managers import *
from .constants import *
from django.urls import reverse

class User(AbstractUser):
    username = None
    role = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20, unique=True)
    town = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', blank=True, null=True, default='images/no_photo.png')
    birthday = models.DateField()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_absolute_url(self):
        return reverse("account/account_details")


class Employee(User):
    class Meta:
        proxy = True

    objects = EmployeeManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = EMPLOYEE
        return super().save(*args, **kwargs)


class Client(User):
    class Meta:
        proxy = True

    object = ClientManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = CLIENT
        return super().save(*args, **kwargs)


# Create your models here.
class Company(models.Model):
    name  = models.CharField(max_length=150)
    logo  = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    address  = models.CharField(max_length=150)
    email    = models.EmailField()
    creation = models.DateField()


class News(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    description = models.CharField(max_length=150)

    def get_absolute_url(self):
         return reverse('news_detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class TermsDictionary(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date = models.DateField()


class Vacation(models.Model):
    position = models.CharField(max_length=150, unique=True)
    description = models.TextField()

    def get_absolute_url(self):
         return reverse('vacation_detail', args=[str(self.id)])

    def __str__(self):
        return self.position


class Feedback(models.Model):
    title = models.CharField(max_length=150)
    mark = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    date = models.DateField()


class ToyType(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
 
    def get_absolute_url(self):
         return reverse('toys_list_by_type', args=[self.slug])

    def __str__(self):
        return self.name


class Toy(models.Model):
    name = models.CharField(max_length=150, unique=True)
    price = models.FloatField()
    toy_type = models.ForeignKey(ToyType, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    produced = models.BooleanField()

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
         return reverse('toy_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Promocode(models.Model):
    name = models.CharField(max_length=150)
    discount  = models.FloatField()
    is_active = models.BooleanField()

    def get_absolute_url(self):
         return reverse('promocode_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Order(models.Model):
    order_date  = models.DateField()
    finish_date = models.DateField()
    #client = models.OneToOneField(Client, on_delete=models.SET_NULL, null=True)
    toy = models.ForeignKey(Toy, null=True, on_delete=models.SET_NULL)
    toy_count = models.IntegerField()
    promocodes = models.ManyToManyField(Promocode)

    def get_absolute_url(self):
         return reverse('order_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.code)

    
class PickUpPoints(models.Model):
    point = models.CharField(max_length=150)