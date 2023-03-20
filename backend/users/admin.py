from django.contrib import admin

from .models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    empty_value_display = 'отсутствует'
    list_display = ('username', 'first_name', 'last_name', 'email')
    ordering = ['username']
    search_fields = ['username', 'email']


class SucscribeAdmin(admin.ModelAdmin):
    empty_value_display = 'отсутствует'
    list_display = ('subscribing', 'subscriber')
    ordering = ['subscribing']
    search_fields = ['subscribing', 'subscriber']


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SucscribeAdmin)
