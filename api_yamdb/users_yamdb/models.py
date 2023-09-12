from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField('Biography', blank=True)
    role = models.CharField(
        max_length=max([len(x) for (x, _) in ROLES]),
        choices=ROLES,
        default=USER
    )

    class Meta:
        ordering = ('date_joined',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
# property убрали, пошли по пути констант ADMIN, MODERATOR, USER
