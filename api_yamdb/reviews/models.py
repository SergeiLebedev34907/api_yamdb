from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название категории')
    slug = models.SlugField(
        unique=True,
        verbose_name='Краткое название'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название жанра')
    slug = models.SlugField(
        unique=True,
        verbose_name='Краткое название'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название произведения')
    category = models.ForeignKey(
        Category,
        blank=True, null=True,
        related_name='titles',
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Произведене'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.title


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='tg_title',
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        blank=True, null=True,
        related_name='th_genre',
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    score = models.IntegerField()
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.title} {self.user} {self.mark}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )
    text = models.TextField(
        max_length=400,
        verbose_name='Комментарий',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
