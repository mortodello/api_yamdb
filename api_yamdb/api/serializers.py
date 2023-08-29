from rest_framework import serializers
from api.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ['id', 'title', 'score', 'text', 'author', 'pub_date']
        read_only_fields = ['id', 'author', 'pub_date']
