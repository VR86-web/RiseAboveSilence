from django import forms
from django_countries.widgets import CountrySelectWidget

from RiseAboveSilence.accounts.mixins import DisableFieldsMixin
from RiseAboveSilence.accounts.models import Profile


class ProfileBaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'country': CountrySelectWidget(attrs={'class': 'form-control'}),
        }


class ProfileCreateForm(ProfileBaseForm):
    pass


class ProfileEditForm(ProfileBaseForm):
    pass


class ProfileDeleteForm(ProfileBaseForm, DisableFieldsMixin):
    disabled_fields = ('__all__',)
