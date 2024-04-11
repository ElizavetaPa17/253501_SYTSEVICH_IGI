from django.contrib import admin
from .models import *

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'birthday')
    list_filter = ('birthday',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'product_type', 'produced')
    list_filter = ('price', 'product_type', 'produced')


class OrderInlines(admin.TabularInline):
    model = Order


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'town', 'address', 'employee')
    list_filter = ('town', 'employee')
    inlines = [OrderInlines]


class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'is_active')
    list_filter = ('discount', 'is_active')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_date', 'finish_date', 'client', 'product', 'product_count', 'promocode')
    list_filter = ('order_date', 'finish_date', 'client', 'product', 'product_count', 'promocode')


admin.site.register(Employee,    EmployeeAdmin)
admin.site.register(Product,     ProductAdmin)
admin.site.register(Order,       OrderAdmin)
admin.site.register(Promocode,   PromocodeAdmin)