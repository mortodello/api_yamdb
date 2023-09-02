from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Categories, Genres, Titles
from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesGetSerializer,
    TitlesPostSerializer
)


# без пермишенов ))
class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    # permission_classes = (Administrator,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    # permission_classes = (Administrator,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesGetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    pagination_class = PageNumberPagination
    # permission_classes = (Administrator,)

    def get_serializer_class(self):
        # здесь будет выбор сериализатора, пока в работе
        if self.action == 'create':
            return TitlesPostSerializer
        # if self.action == 'update':
        #    return TitlesPostSerializer
        # if self.action == 'partial_update':
        #    return TitlesPostSerializer
        return TitlesGetSerializer
