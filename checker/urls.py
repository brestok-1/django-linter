from django.urls import path

from checker.views import IndexView

app_name = 'checker'

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]