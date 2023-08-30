from rest_framework import serializers
from reviews.models import Review, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'review', 'text', 'author', 'pub_date']
        read_only_fields = ['id', 'pub_date']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ['id', 'title', 'score', 'text', 'author', 'pub_date']
        read_only_fields = ['id', 'author', 'pub_date']
