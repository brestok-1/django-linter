from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

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
