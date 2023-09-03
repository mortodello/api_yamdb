from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)

class YaMDBUser(AbstractUser):
    bio = models.TextField('Biography', blank=True)
    role = models.CharField(max_length=16, choices=CHOICES, default='user')

    def __str__(self):
        return self.username
