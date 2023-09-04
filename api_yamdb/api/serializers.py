from datetime import date
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (Categories, Genres, Titles,
                            Review, Comment)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(queryset=Categories.objects.all(),
                                slug_field='slug', required=True)
    genre = SlugRelatedField(queryset=Genres.objects.all(),
                             slug_field='slug', required=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Titles

    # валидатор для года на уровне сериализатора
    def validate_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Произведения из будущего не принимаются!')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategoriesSerializer(
            instance.category).data
        representation['genre'] = GenresSerializer(
            instance.genre.all(), many=True).data
        return representation

    def get_rating(self, obj):
        score = 0
        count = 0
        ratings = obj.reviews.all()
        for rating in ratings:
            score += rating.score
            count += 1
        if score == 0:
            return None
        return int(score / count)


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
        fields = ['id', 'score', 'text', 'author', 'pub_date']
        read_only_fields = ['id', 'author', 'pub_date', 'title']
