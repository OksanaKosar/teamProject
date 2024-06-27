from django.contrib.auth import logout, login

from django.contrib.auth.views import LoginView

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from bmp.models import BMPImage
from user_management.forms import RegisterUserForm, LoginUserForm


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "user_management/register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('about_program')


class LoginUser(LoginView):

    form_class = LoginUserForm
    template_name = 'user_management/login.html'

    def get_success_url(self):
        last_image = BMPImage.objects.filter(user=self.request.user).order_by('-id').first()
        if last_image:
            return reverse_lazy('image_detail', kwargs={'image_id': last_image.id})
        else:
            return reverse_lazy('about_program')


def logout_user(request):
    logout(request)
    return redirect('login')
