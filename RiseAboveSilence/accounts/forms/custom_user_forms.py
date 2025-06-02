from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from RiseAboveSilence.accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):
    pass