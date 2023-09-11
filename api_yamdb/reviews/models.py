from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from .validators import year_validator

User = get_user_model()

MIN_RATING = 1
MAX_RATING = 10
REVIEW_TEXT_PRESENTATION_LENGTH = 50
CATEGORIES_GENRES_TITLES_NAME_LENGTH = 256
CATEGORIES_GENRES_SLUG_LENGTH = 56


class CategoriesGenresBase(models.Model):
    name = models.CharField(max_length=CATEGORIES_GENRES_TITLES_NAME_LENGTH)
    slug = models.SlugField(unique=True,
                            max_length=CATEGORIES_GENRES_SLUG_LENGTH)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class ReviewCommentBase(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)ss'
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:REVIEW_TEXT_PRESENTATION_LENGTH]


class Categories(CategoriesGenresBase):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(CategoriesGenresBase):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=CATEGORIES_GENRES_TITLES_NAME_LENGTH)
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
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenresTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(ReviewCommentBase):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            MIN_RATING, message='Оценка должна быть не меньше 1.'),
            MaxValueValidator(
                MAX_RATING, message='Оценка должна быть не больше 10.')]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('title', 'author')


class Comment(ReviewCommentBase):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
