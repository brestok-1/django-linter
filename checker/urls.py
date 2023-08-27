from django.urls import path

from checker.views import IndexView, FilesView, DeleteFileView, UpdateFileView, GetCheckResult

app_name = 'checker'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('files/', FilesView.as_view(), name='files'),
    path('file/delete/<int:file_id>', DeleteFileView.as_view(), name='delete'),
    path('update/<int:pk>', UpdateFileView.as_view(), name='update'),
    path('file/result/<int:pk>', GetCheckResult.as_view(), name='result')
]
