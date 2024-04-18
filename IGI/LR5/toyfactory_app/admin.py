from django.contrib import admin
from .models import *

# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'mark', 'date')
    list_filter = ('mark', 'date')


class EmployeeAdmin(admin.ModelAdmin):
    add_fieldsets = ('role', 'first_name', 'last_name', 'email', 'phone', 'address', 'birthday')
    list_filter = ('birthday', 'town')
 

class UsersRelationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_owner')


class ToyTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}


class ToyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'toy_type', 'produced')
    list_filter = ('price', 'toy_type', 'produced')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    add_fieldsets = ('role', 'first_name', 'last_name', 'email', 'phone', 'address', 'birthday')
    list_filter = ('birthday', 'town',)


class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'promocode_type')
    list_filter = ('discount', 'promocode_type')


class PromocodeTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_date', 'finish_date', 'toy', 'toy_count')
    list_filter = ('order_date', 'finish_date', 'toy', 'toy_count', 'promocodes')


class PickUpPointsAdmin(admin.ModelAdmin):
    list_display = ('point',)


admin.site.register(Company)
admin.site.register(News)
admin.site.register(TermsDictionary)
admin.site.register(Vacation)
admin.site.register(Feedback,       FeedbackAdmin)
admin.site.register(Employee,       EmployeeAdmin)
admin.site.register(UsersRelations, UsersRelationsAdmin)
admin.site.register(ToyType,        ToyTypeAdmin)
admin.site.register(Toy,            ToyAdmin)
admin.site.register(Order,          OrderAdmin)
admin.site.register(Promocode,      PromocodeAdmin)
admin.site.register(PromocodeType,  PromocodeTypeAdmin)
admin.site.register(PickUpPoints,   PickUpPointsAdmin)