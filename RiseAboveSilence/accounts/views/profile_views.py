from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView

from RiseAboveSilence.accounts.forms import ProfileEditForm, ProfileDeleteForm
from RiseAboveSilence.accounts.models import Profile


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts_templates/profile-template.html"


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts_templates/profile-edit-template.html"

    def get_success_url(self):
        return reverse_lazy("profile-details", kwargs={"pk": self.object.pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = "accounts_templates/profile-delete-template.html"

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        user = profile.user
        profile.delete()
        user.delete()  # also logs the user out automatically
        return redirect("index")  # home page

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
