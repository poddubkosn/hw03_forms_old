from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView
# from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import CreationForm

from django.contrib.auth import get_user_model


User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class MyPasswordChange(PasswordChangeView):
    success_url = reverse_lazy('users:password_change_done_form')
    template_name = 'users/password_change_form.html'


# class MyPasswordResetConfirmView(PasswordResetConfirmView):
#     success_url = reverse_lazy('users:reset_complete')
#     template_name = 'users/password_reset_confirm.html'
