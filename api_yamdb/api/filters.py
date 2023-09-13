import django_filters

from reviews.models import Categories, Genres, Title


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter()
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Categories.objects.all().prefetch_related('titles'),
        to_field_name='slug'
    )
    genre = django_filters.ModelChoiceFilter(
        field_name='genre',
        queryset=Genres.objects.all().prefetch_related('titles'),
        to_field_name='slug'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
