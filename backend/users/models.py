from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from users.validators import validate_username


class User(AbstractUser):

    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        max_length=settings.USERNAME_MAX_LEN,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'[\w.@+_-]+',
                message='Допустим ввод букв и символов из числа ".@+-_"'
            ),
            validate_username
        ]
    )

    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=settings.EMAIL_MAX_LEN,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.FIRST_NAME_MAX_LEN,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.LAST_NAME_MAX_LEN,
    )

    password = models.CharField(
        'Пароль',
        max_length=settings.PASSWORD_MAX_LEN,
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber'
    )
    subscribing = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор подписки',
        related_name='subscribing',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscribing'],
                name='unique_subscribe'
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_subscribe",
                check=~models.Q(subscriber=models.F("subscribing")),
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (
            f'{self.subscriber} подписан на {self.subscribing}'
        )
