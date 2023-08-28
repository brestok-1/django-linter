import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# from checker.tasks import check_file_errors


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
            task = check_file_errors.delay(self.id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'file_check',
                {
                    'type': 'open_websocket',
                    'task_id': task.task_id,
                }
            )

            # Запуск celery task и передача id загруженного файла

# @receiver(post_save, sender=UploadedFile)
# def update_check_result(sender, instance, **kwargs):
#     # Обновляем поле check_result после выполнения celery task
#     try:
#         # updated_instance = UploadedFile.objects.get(id=instance.id)
#         # updated_instance.check_result = instance.check_result
#         # updated_instance.save(update_fields=['check_result'])
#         # Отправляем сообщение о завершении задачи по websocket
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'file_check',
#             {
#                 'type': 'task_finished',
#                 'task_id': str(instance.id),
#                 'result': instance.check_result,
#             }
#         )
#     except ObjectDoesNotExist:
#         pass
