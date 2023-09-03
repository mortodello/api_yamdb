from rest_framework import serializers
from datetime import date

from reviews.models import Categories, Genres, Titles, GenresTitles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genres


# этот сериализатор для просмотра, в нем данные отображаются как в таблице
class TitlesGetSerializer(serializers.ModelSerializer):
    # эти поля отображают объекты соответствующих таблиц согласно ТЗ
    # поэтому тип - сериализатор
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)
    # это поле будет создаваться на лету, т.к. рейинг непостоянен
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Titles

    def get_rating(self, obj):
        rating_list = []
        score = 0
        ratings = obj.reviews.all()
        for rating in ratings:
            rating_list.append(rating.score)
        for i in rating_list:
            score += i
        if len(rating_list) == 0:
            return 0
        return int(score / len(rating_list))


# этот сериализатор для создания/изменения,
# в нем категория и жанр выбираются из предложенного
class TitlesPostSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Categories.objects.all())
    genre = serializers.MultipleChoiceField(choices=Genres.objects.all())

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Titles

    # валидатор для года на уровне сериализатора
    def validate_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Произведения из будущего не принимаются!')
        return value
