import json
import time

from asgiref.sync import async_to_sync
from celery.signals import task_postrun
from channels.layers import get_channel_layer
from pylint import epylint as lint
from celery import shared_task
from celery.utils.log import get_task_logger
from celery.result import AsyncResult

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
    time.sleep(5)
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



# @task_postrun.connect
# def task_postrun_handler(task_id, **kwargs):

