from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


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
    confirmation_code = models.CharField(
        max_length=36,
        blank=True,
        null=True
    )


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=250)
    year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=700, blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='titles')

    def __str__(self):
        return self.name


class Rating(models.Model):
    value = models.PositiveSmallIntegerField(
        "Рейтинг",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    
    def __str__(self):
        return self.value


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    score = models.ForeignKey(
        Rating,
        on_delete=models.PROTECT,
        related_name='reviews',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.CharField(max_length=1000)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True,
    )
