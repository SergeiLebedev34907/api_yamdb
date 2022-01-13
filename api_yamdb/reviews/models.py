from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERS_ROLE = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    )

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.CharField(max_length=400, blank=True, null=True)
    role = models.CharField(max_length=9, choices=USERS_ROLE, default="user")

    class Meta:
        ordering = ["date_joined"]


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="Краткое название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название жанра")
    slug = models.SlugField(unique=True, verbose_name="Краткое название")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    title = models.CharField(
        max_length=200, verbose_name="Название произведения"
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name="titles",
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Произведене"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.title


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        related_name="tg_title",
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        related_name="th_genre",
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    MARK_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
    ]
    mark = models.CharField(
        max_length=2,
        choices=MARK_CHOICES,
        blank=True,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name="reviews",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.title} {self.user} {self.mark}"


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата комментария"
    )
    text = models.TextField(
        max_length=400,
        verbose_name="Комментарий",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]