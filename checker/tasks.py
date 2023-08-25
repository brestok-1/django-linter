from celery.signals import task_postrun
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
    print(output)
    return output