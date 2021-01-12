from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserRoles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name='Роль пользователя',
    )
    email = models.EmailField(
        max_length=128,
        blank=False,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        default=email,
        blank=True,
        verbose_name='Логин',
    )
    # confirmation_code = models.CharField(
    #     max_length=255,
    #     unique=True
    # )
    first_name = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе',
    )
