import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.py']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Acceptable file extensions: .py')


# Create your models here.
class UploadedFile(models.Model):
    NEW = 'new'
    DELETED = 'deleted'
    OVERWRITTEN = 'overwritten'
    STATUS_CHOICES = [
        (NEW, 'New'),
        (DELETED, 'Deleted'),
        (OVERWRITTEN, 'Overwritten'),
    ]

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    file = models.FileField(validators=[validate_file_extension], upload_to='media/%(user)s/')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    check_result = models.TextField(default='')

    def __str__(self):
        return f'{self.file} uploaded by {self.user}'
