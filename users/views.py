from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegistrationForm


# Create your views here.
class LoginUserView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = 'Thanks for authorisation, %(username)s!'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, username=self.request.user)


class RegisterUserView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('account:login')
    success_message = "%(username)s was created successfully"
    title = 'Store - Sign Up'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, username=self.object)


@login_required
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse('checker:index'))
