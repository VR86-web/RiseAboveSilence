from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from RiseAboveSilence.accounts.forms import CustomUserCreationForm

UserModel = get_user_model()


class CustomUserLoginView(LoginView):
    template_name = 'accounts_templates/login.html'


class CustomUserRegisterView(CreateView):
    model = UserModel
    template_name = 'accounts_templates/registration-template.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return response


