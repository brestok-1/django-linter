import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
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
    NEW = 'Новый'
    DELETED = 'Удален'
    OVERWRITTEN = 'Перезаписан'
    STATUS_CHOICES = [
        (NEW, 'New'),
        (DELETED, 'Deleted'),
        (OVERWRITTEN, 'Overwritten'),
    ]
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='user')
    file = models.FileField(upload_to=upload_to, validators=[validate_file_extension])
    filename = models.CharField(max_length=64, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    check_result = models.TextField(default='')

    def __str__(self):
        return self.file.name

    def save(self, task_need=True, *args, **kwargs):
        self.filename = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)
        # task_need = kwargs['task_need']
        if task_need:
            from .tasks import check_file_errors
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                'file_check',
                {
                    'type': 'task_message',
                    'message': {
                        'message': 'New task',
                        'result': '',
                    },
                }
            )
            check_file_errors.apply_async(args=[self.id], queue='file_check')
        super().save(*args, **kwargs)

