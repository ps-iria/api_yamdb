from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
        db_index=True,
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        verbose_name='Логин',
    )
    first_name = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе',
    )
    confirmation_code = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
        null=True,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR


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

    def get_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()])

    def __str__(self):
        return (f' name: {self.name},'
                f' year: {self.year},'
                f' genre: {self.get_genre()},'
                f' category: {self.category}'
                )


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
    score = models.IntegerField(
        'review score',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        unique_together = ["title", "author"]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.text
