from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class YaMDBUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    bio = models.TextField('Biography', blank=True)
    role = models.CharField(max_length=16, choices=CHOICES, default='user')
    confirmation_code = models.CharField(max_length=6, blank=True)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return ({
            'refresh': str(refresh),
            'refresh': str(refresh.access_token),
        })

    def __str__(self):
        return self.username
