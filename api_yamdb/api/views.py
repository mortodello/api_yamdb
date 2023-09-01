from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from api.serializers import CommentSerializer
from .permissions import AuthorOrReadOnly, Moderator, Administrator
from reviews.models import Review


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AuthorOrReadOnly, Moderator, Administrator]

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)
