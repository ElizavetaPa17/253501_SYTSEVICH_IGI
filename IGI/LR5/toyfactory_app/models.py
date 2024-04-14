from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    name  = models.CharField(max_length=150)
    logo  = models.ImageField(null=True)
    video = models.FileField(null=True,
                            validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    address  = models.CharField(max_length=150)
    email    = models.EmailField()
    creation = models.DateField()


class News(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(null=True)
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


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=(('Client', 'Client'), ('Employee', 'Employee')))
    image = models.ImageField(null=True)
    phone = models.CharField(max_length=25, unique=True)
    birthday = models.DateField()

    def get_absolute_url(self):
         return reverse('employee_detail', args=[str(self.id)])

    def __str__(self):
        return self.user.username


class ToyType(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
 
    def __str__(self):
        return self.name


class Toy(models.Model):
    name = models.CharField(max_length=150, unique=True)
    price = models.FloatField()
    toy_type = models.ForeignKey(ToyType, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(null=True)
    produced = models.BooleanField()

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
         return reverse('toy_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=(('Client', 'Client'), ('Employee', 'Employee')))
    phone = models.CharField(max_length=25, unique=True)
    town  = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    employee = models.ManyToManyField(Employee)

    def get_absolute_url(self):
         return reverse('client_detail', args=[str(self.id)])

    def __str__(self):
        return self.user.username


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
    client = models.OneToOneField(Client, on_delete=models.SET_NULL, null=True)
    toy = models.ForeignKey(Toy, null=True, on_delete=models.SET_NULL)
    toy_count = models.IntegerField()
    promocodes = models.ManyToManyField(Promocode)

    def get_absolute_url(self):
         return reverse('order_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.code)

    
class PickUpPoints(models.Model):
    point = models.CharField(max_length=150)