from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = "accounts_templates/profile-delete-template.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == "GET":
            context["form"] = ProfileDeleteForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)
