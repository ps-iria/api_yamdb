from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    pass


class Genre(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    pass


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
    pass
