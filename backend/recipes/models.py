from django.core.validators import MinValueValidator
from django.db import models
# from django.conf import settings
from users.models import CustomUser


class Recipe(models.Model):
    """ Рецепты. Основная модель.
    Имеет связи через related_name c объектами других моделей:
    author --> CustomUser,
    ingredients --> Ingredient,
    ingredient_list --> IngredientsinRecipt,
    tags --> Tag,
    favourites --> Favourite,
    shop_list --> Shopping_list,
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    text = models.CharField(
        max_length=250,
        verbose_name='Текстовое описание'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(1, 'Значение не может быть меньше 1')
        ]
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes',
        through='IngredientsinRecipt',
        verbose_name='Ингредиент',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Тэг',
    )
    # image =

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Ингридиенты для рецептов.
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientsinRecipt(models.Model):
    """ Промежуточная модель для связи инридиентов с рецептом.
    Добавляет поле количество для ингридиента.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Значение не может быть меньше 1')
        ]
    )


class Tag(models.Model):
    """ Тэги
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой HEX-код',
        unique=True,

    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Favourite(models.Model):
    """ Избранные рецепты пользователя.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Избранное'

    def __str__(self):
        return {self.user}


class Shopping_list(models.Model):
    """ Список покупок.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Список покупок'

    def __str__(self):
        return (
            f'{self.user} добавил "{self.recipe}" в Список покупок'
        )
