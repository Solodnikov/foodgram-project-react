from django.contrib import admin
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('username', 'first_name', 'last_name', 'email')
    ordering = ['username']
    search_fields = ['username', 'email']


admin.site.register(CustomUser, CustomUserAdmin)
