import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


def upload_to(instance, filename):
    return '{}/{}'.format(instance.user.username, filename)


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

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='user')
    file = models.FileField(upload_to=upload_to, validators=[validate_file_extension])
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    check_result = models.TextField(null=True)

    def __str__(self):
        return self.file.name