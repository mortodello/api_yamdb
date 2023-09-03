from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from users_yamdb.permissions import AuthorOrReadOnly, Moderator, Administrator
from reviews.models import Categories, Genres, Titles, Review, Comment
from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesGetSerializer,
    TitlesPostSerializer,
    ReviewSerializer,
    CommentSerializer
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
        return TitlesGetSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    # permission_classes = [AuthorOrReadOnly, Moderator, Administrator]

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (AuthorOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.kwargs['title_id'])
