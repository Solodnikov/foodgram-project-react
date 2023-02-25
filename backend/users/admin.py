from django.contrib import admin

from .models import CustomUser, Sucscribe


class CustomUserAdmin(admin.ModelAdmin):
    empty_value_display = 'отсутствует'
    list_display = ('username', 'first_name', 'last_name', 'email')
    ordering = ['username']
    search_fields = ['username', 'email']


class SucscribeAdmin(admin.ModelAdmin):
    empty_value_display = 'отсутствует'
    list_display = ('subscribing', 'subscriber')
    ordering = ['subscribing']
    search_fields = ['subscribing', 'subscriber']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Sucscribe, SucscribeAdmin)
