from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import YaMDBUser

fields = list(UserAdmin.fieldsets)
fields[1] =  ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'role')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(YaMDBUser, UserAdmin) 