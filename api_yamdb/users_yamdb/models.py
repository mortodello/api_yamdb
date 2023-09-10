from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField('Biography', blank=True)
    role = models.CharField(
        max_length=max([len(x) for (x, _) in ROLES]),
        choices=ROLES,
        default=ROLES[0][0]
    )
    admin = models.BooleanField(default=False)
    moderator = models.BooleanField(default=False)

    class Meta:
        ordering = ('date_joined',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.admin = (self.role == 'admin')
        self.moderator = (self.role == 'moderator')
        super(CustomUser, self).save(*args, **kwargs)

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_moderator(self):
        """Is the user a moderator member?"""
        return self.moderator
