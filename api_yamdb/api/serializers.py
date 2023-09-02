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
        # здесь будет метод подсчёта рейтинга
        # пока заглушка возвращает 10
        return 10


# этот сериализатор для создания/изменения,
# в нем категория и жанр выбираются из предложенного
class TitlesPostSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Categories.objects.all())
    genre = serializers.MultipleChoiceField(choices=Genres.objects.all())

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Titles

    # тип поля сериализатор не подходит для записи,
    # надо указать явно, что куда записывать
    def create(self, validated_data):
        validated_data.pop('genre')
        title = Titles.objects.create(**validated_data)
        # здесь будет код для сохранения жанров
        return title

    def update():
        ...

    # валидатор для года на уровне сериализатора
    def validate_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Произведения из будущего не принимаются!')
        return value
