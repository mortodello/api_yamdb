from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CustomUser

EMAIL_LENGTH = 254
USERNAME_LENGTH = 150


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True,
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
        ]
    )

    def validate_username(self, value):
        import re

        if value == 'me':
            raise serializers.ValidationError('This is username forbidden.')

        for ch in value:
            if not re.search(r'^[\w.@+-]+\Z$', ch):
                raise serializers.ValidationError(
                    f'Character {ch} forbidden in username.'
                )
        return value

    def validate_email(self, value):
        if self.instance:
            initial_email = self.instance.email
            if initial_email and initial_email != value:
                raise serializers.ValidationError(
                    'Change email strictly forbidden!'
                )
        return value

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
