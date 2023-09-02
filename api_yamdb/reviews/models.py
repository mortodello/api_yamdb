from django.db import models

from .validators import year_validator


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=56)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=56)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    # добавил валидатор на уровне модели
    year = models.IntegerField(validators=(year_validator,),)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        through='GenresTitles'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведния'

    def __str__(self):
        return self.name


class GenresTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Titles, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.genre} {self.title}'
