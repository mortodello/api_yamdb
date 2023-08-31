from rest_framework import serializers

from .models import YaMDBUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = YaMDBUser
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']