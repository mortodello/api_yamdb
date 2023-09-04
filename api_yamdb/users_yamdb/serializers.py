from rest_framework import serializers

from .models import YaMDBUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = YaMDBUser
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']


class UserEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = YaMDBUser
        fields = ['username', 'email', 'confirmation_code']
        # read_only_fields = ['confirmation_code']

    def create(self, validated_data):
        user, created = YaMDBUser.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.confirmation_code = validated_data['confirmation_code']
        user.save(force_update=True)

        return user
