from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):  # we extend base user model and add user image

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        unique_together = ('email',)  # email have to be unique
