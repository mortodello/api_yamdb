
import django_filters

from reviews.models import Categories, Genres, Title


class TitleFilter(django_filters.FilterSet):
    """
    Filtering Title objects. Defines a set of filters that
    can be applied to filter objects of the Title model.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter()
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Categories.objects.all(),
        to_field_name='slug'
    )
    genre = django_filters.ModelChoiceFilter(
        field_name='genre',
        queryset=Genres.objects.all(),
        to_field_name='slug'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
