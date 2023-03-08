from django.db import models
from django.contrib.auth.models import AbstractUser


# from django.conf import settings
# Create your models here.


class CustomUser(AbstractUser):

    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        max_length=150,
        unique=True,
        # validators=[validate_username]
    )

    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=254
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        # validators=[validate_username]
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        # validators=[validate_username]
    )

    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user'),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber'
    )
    subscribing = models.ForeignKey(
        CustomUser,
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
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (
            f'{self.subscriber} подписан на {self.subscribing}'
        )
