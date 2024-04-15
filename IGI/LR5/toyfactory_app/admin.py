from django.contrib import admin
from .models import *

# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'mark', 'date')
    list_filter = ('mark', 'date')


class EmployeeAdmin(admin.ModelAdmin):
    add_fieldsets = ('first_name', 'last_name', 'email', 'phone', 'image', 'birthday')
    list_filter = ('birthday',)


class ToyTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}


class ToyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'toy_type', 'produced')
    list_filter = ('price', 'toy_type', 'produced')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    add_fieldsets = ('first_name', 'last_name' 'email', 'phone', 'town', 'address')
    list_filter = ('town',)


class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'is_active')
    list_filter = ('discount', 'is_active')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_date', 'finish_date', 'toy', 'toy_count')
    list_filter = ('order_date', 'finish_date', 'toy', 'toy_count', 'promocodes')


admin.site.register(Company)
admin.site.register(News)
admin.site.register(TermsDictionary)
admin.site.register(Vacation)
admin.site.register(Feedback,  FeedbackAdmin)
admin.site.register(Employee,  EmployeeAdmin)
admin.site.register(ToyType,   ToyTypeAdmin)
admin.site.register(Toy,       ToyAdmin)
admin.site.register(Order,     OrderAdmin)
admin.site.register(Promocode, PromocodeAdmin)