from django.contrib.admin import ModelAdmin, register
from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_admin', 'is_moderator')
    search_fields = ('email', 'username')
