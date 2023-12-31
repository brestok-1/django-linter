from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from django.conf import settings
from pylint import epylint as lint
from celery import shared_task
from celery.utils.log import get_task_logger

from checker.models import UploadedFile

logger = get_task_logger('__name__')


@shared_task
def check_file_errors(file_id):
    file = UploadedFile.objects.get(id=file_id)
    (pylint_stdout, pylint_stderr) = lint.py_run(f"{file.file.path}"
                                                 f" --disable=import-error,"
                                                 f"missing-module-docstring,"
                                                 f"missing-function-docstring,"
                                                 f"missing-class-docstring "
                                                 f"--max-line-length=120", return_std=True)
    output = pylint_stdout.getvalue()
    logger.info(output)
    file.check_result = str(output)
    file.save(task_need=False)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'file_check',
        {
            'type': 'task_message',
            'message': {
                'message': 'Task completed',
                'result': output
            },
        }
    )
    send_email_notification.apply_async(args=[file_id], queue='email_send')


@shared_task
def send_email_notification(file_id):
    file = UploadedFile.objects.get(id=file_id)
    subject = f'Здравствуйте! Проверка {file.filename} проведена успешно!'
    message = (f'Результат проверки:\n'
               f'{file.check_result}')
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[file.user.email]
    )
    logger.info('Результат проверки отправлен на почту')
    file.is_send_result = True
    file.save(task_need=False)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'email_send',
        {
            'type': 'email_message',
            'message': 'Result send',
        }
    )
