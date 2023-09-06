from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

from .models import YaMDBUser


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=YaMDBUser.objects.all())]    
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(queryset=YaMDBUser.objects.all()),
            RegexValidator(regex='^[\w.@+-]+\Z')
        ]    
    )
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('This is username forbidden.')
        return value
    
    def validate_email(self, value):
        if self.instance:
            initial_email = self.instance.email
            if initial_email and initial_email != value:
                raise serializers.ValidationError('Change email strictly forbidden!')
        return value

    class Meta:
        model = YaMDBUser
        fields = ['username', 'email', 'role', 'first_name', 'last_name', 'bio']

