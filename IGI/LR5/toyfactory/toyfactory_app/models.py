from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=150)
    code = models.BigIntegerField()
    phone = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    code = models.BigIntegerField()
    price = models.FloatField()
    product_type = models.ForeignKey(ProductType, null=True, on_delete=models.SET_NULL)
    produced = models.BooleanField()

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=150)
    code = models.BigIntegerField()
    phone = models.CharField(max_length=25)
    town  = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Promocode(models.Model):
    name = models.CharField(max_length=150)
    discount  = models.FloatField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.name


class Order(models.Model):
    code = models.BigIntegerField()
    order_date  = models.DateField()
    finish_date = models.DateField()
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    product_count = models.IntegerField()
    promocode = models.ForeignKey(Promocode, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.code)