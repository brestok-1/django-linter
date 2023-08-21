from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class AdminCustomUser(UserAdmin):
    list_display = ('username', 'email',)
    list_display_links = ('username',)
    search_fields = ('username', 'email')
