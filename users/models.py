from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):  # we extend base user model and add user image
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        unique_together = ('email',)  # email have to be unique
