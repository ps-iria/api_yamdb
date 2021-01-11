from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

class Title(models.Model):
    pass


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
