from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    USER_ROLES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
    )

    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=settings.EMAIL_MAX_LEN
    )

    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        max_length=settings.USERNAME_MAX_LEN,
        unique=True,
        # validators=[validate_username]
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.USERNAME_MAX_LEN,
        # validators=[validate_username]
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.USERNAME_MAX_LEN,
        # validators=[validate_username]
    )

    # "is_subscribed": false

    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in USER_ROLES),
        default=USER,
        choices=USER_ROLES
    )

    password = models.CharField(
        'Пароль',
        max_length=settings.PASSWORD_MAX_LEN,
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user'),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff
