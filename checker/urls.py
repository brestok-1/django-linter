from django.urls import path

from checker.views import IndexView, FilesView

app_name = 'checker'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('files/', FilesView.as_view(), name='files'),
]