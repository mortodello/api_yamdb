from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from users_yamdb.permissions import (AdminOrReadOnly,
                                     AuthorOrHasRoleOrReadOnly)
from reviews.models import Categories, Genres, Title, Review
from api.serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)


class CategoriesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self, slug=None):
        if slug:
            return get_object_or_404(Categories, slug=slug)
        return Categories.objects.all()


class GenresViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self, slug=None):
        if slug:
            return get_object_or_404(Genres, slug=slug)
        return Genres.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year')
    pagination_class = PageNumberPagination
    permission_classes = [AdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = Title.objects.all()
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        return queryset


class BaseCommentReviewViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [AuthorOrHasRoleOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']


class CommentViewSet(BaseCommentReviewViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)


class ReviewViewSet(BaseCommentReviewViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title,
                                                id=self.kwargs['title_id']))
