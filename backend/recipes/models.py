from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Recipe(models.Model):
    """ Рецепты. Основная модель."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Zа-яА-Я- ]+$',
                message='Ввод символов, не являющихся буквами, не допустимо',
            )
        ]
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    text = models.CharField(
        max_length=250,
        verbose_name='Текстовое описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(1, 'Значение не может быть меньше 1')
        ]
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Тэг',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/',
        blank=True,
        null=True,
        default=None,
    )

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
        verbose_name='Название',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Zа-яА-Я- ]+$',
                message='Ввод символов, не являющихся буквами, не допустимо',
            )
        ]
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='ingredient_unique'
            )
        ]

    def __str__(self):
        return (
            f'"{self.name}" c мерой измерения "{self.measurement_unit}".')


class AmountOfIngredient(models.Model):
    """ Модель количества ингредиентов.
    Связана с моделью рецептов.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        related_name='amount_of_ingredient',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Значение не может быть меньше 1')
        ]
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredients',
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            UniqueConstraint(
                fields=('ingredient', 'amount',),
                name='unique_ingredient_amount',
            ),
        )

    def __str__(self):
        return (
            f'{self.ingredient.name} - {self.amount}'
            f' ({self.ingredient.measurement_unit})'
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
        validators=[
            RegexValidator(
                regex=r'^#([A-Fa-f0-9]{3,6})$',
                message='Cимволы не соответствуют цветовому HEX-коду',
            )
        ]

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
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='+',
    )

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return (
            f'{self.user} добавил "{self.recipe}" в Избранные рецепты.')


class ShoppingList(models.Model):
    """ Список покупок.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='+',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return (
            f'{self.user} добавил "{self.recipe}" в Список покупок.'
        )
