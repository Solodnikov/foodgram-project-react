from django.contrib import admin

from .models import (AmountOfIngredient, Favourite, Ingredient, Recipe,
                     ShoppingList, Tag)


class AmountOfIngredientInline(admin.TabularInline):
    model = AmountOfIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = 'отсутствует'
    list_display = ('id', 'name', 'author', 'cooking_time')
    ordering = ['name']
    search_fields = ['name', ]
    inlines = [AmountOfIngredientInline]


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
admin.site.register(Favourite)
admin.site.register(ShoppingList)
