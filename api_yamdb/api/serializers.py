from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from .validators import username_validator, year_validator
from reviews.models import (Categories, Genres, Title,
                            Review, Comment)
from users_yamdb.models import CustomUser

EMAIL_LENGTH = 254
USERNAME_LENGTH = 150
MIN_RATING = 1
MAX_RATING = 10


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(queryset=Categories.objects.all(),
                                slug_field='slug', required=True)
    genre = SlugRelatedField(queryset=Genres.objects.all(),
                             slug_field='slug', required=True, many=True)
    year = serializers.IntegerField(validators=(year_validator,),)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def to_representation(self, instance):
        """Этот метод - альтернатива двум сериализаторам.
           Данные на POST и GET отображаются по разному"""
        representation = super().to_representation(instance)
        representation['category'] = CategoriesSerializer(
            instance.category).data
        representation['genre'] = GenresSerializer(
            instance.genre.all(), many=True).data
        return representation

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg("score"))['score__avg']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'score', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate_score(self, value):
        if value < MIN_RATING or value > MAX_RATING:
            raise ValidationError("Оценка должна быть числом от 1 до 10.")
        return value

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        method = self.context['request'].method
        title = get_object_or_404(Title, id=title_id)

        if method == 'POST' and Review.objects.filter(
            author=author, title=title
        ).exists():
            raise ValidationError(
                'Вы уже оставляли отзыв на это произведение!'
            )

        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
        ]
    )
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
        ]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Этот username запрещён!')
        return username_validator(value)

    def validate_email(self, value):
        if self.instance:
            initial_email = self.instance.email
            if initial_email and initial_email != value:
                raise serializers.ValidationError(
                    'Изменять email запрещено!'
                )
        return value

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
