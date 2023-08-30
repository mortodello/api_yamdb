from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from reviews.models import Title, Comment
from api.serializers import ReviewSerializer, CommentSerializer
from api.permissions import AuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AuthorOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs['title_id'])
