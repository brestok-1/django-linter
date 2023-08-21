from django.urls import path

from users.views import LoginUserView, RegisterUserView, logoutuser

app_name = 'users'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegisterUserView.as_view(), name='register'),
    path('logout/', logoutuser, name='logout'),
]
