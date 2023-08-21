from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegistrationForm


# Create your views here.
class LoginUserView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = 'Thanks for authorisation, %(username)s!'
    title = 'Store - Login'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, username=self.request.user)

class RegisterUserView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = "%(username)s was created successfully"
    title = 'Store - Sign Up'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, username=self.object)

