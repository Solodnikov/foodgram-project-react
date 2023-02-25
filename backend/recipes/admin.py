from django.contrib import admin

from .models import Ingredient, Recipe, Tag, IngredientsinRecipt


class IngredientsinReciptInline(admin.TabularInline):
    model = IngredientsinRecipt
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = 'отсутствует'
    list_display = ('name', 'author', 'cooking_time',)
    # list_display = ('name', 'author', 'cooking_time', 'ingredients', 'tags')
    ordering = ['name']
    search_fields = ['name', ]
    inlines = [IngredientsinReciptInline]


class IngredientAdmin(admin.ModelAdmin):
    empty_value_display = 'отсутствует'
    list_display = ('name', 'measurement_unit')
    ordering = ['name']
    search_fields = ['name', ]


class TagAdmin(admin.ModelAdmin):
    empty_value_display = 'отсутствует'
    list_display = ('name', 'color', 'slug')
    ordering = ['name']
    search_fields = ['name', ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
