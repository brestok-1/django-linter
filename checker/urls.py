from django.urls import path

from checker.views import IndexView, FilesView, DeleteFileView

app_name = 'checker'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('files/', FilesView.as_view(), name='files'),
    path('file/delete/<int:file_id>', DeleteFileView.as_view(), name='delete')
]
