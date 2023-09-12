from django.contrib.admin import ModelAdmin, register

from reviews.models import Categories, Genres, Title, Review, Comment
from users_yamdb.models import CustomUser


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined',
                    'is_admin', 'is_moderator')
    search_fields = ('email', 'username')


@register(Categories)
class CategoriesAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@register(Genres)
class GenresAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@register(Title)
class TitleAdmin(ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name', 'genre', 'category')


@register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('title', 'text', 'score', 'author', 'pub_date')
    search_fields = ('title', 'author', 'pub_date')


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'review')
    search_fields = ('review', 'author', 'pub_date')
