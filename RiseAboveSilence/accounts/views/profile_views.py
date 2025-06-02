
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView

from RiseAboveSilence.accounts.forms import ProfileEditForm, ProfileDeleteForm, ProfileCreateForm
from RiseAboveSilence.accounts.models import Profile


class ProfileCreateView(CreateView):
    model = Profile
    template_name = 'accounts_templates/profile-create-template.html'
    form_class = ProfileCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts_templates/profile-template.html'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts_templates/profile-edit-template.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


class ProfileDeleteView(DeleteView):
    model = Profile
    template_name = 'accounts_templates/profile-delete-template.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            context['form'] = ProfileDeleteForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)
