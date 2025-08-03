from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

from RiseAboveSilence.accounts.forms import ProfileDeleteForm

User = get_user_model()


class ProfileDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.profile = self.user.profile  # <--- fetch existing profile
        self.url = reverse('profile-delete', kwargs={'pk': self.profile.pk})
        self.client.login(username='testuser', password='testpass')

    def test_delete_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_view_context_has_form(self):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)

    def test_delete_view_form_instance_is_correct(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertEqual(form.instance, self.profile)

    def test_delete_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts_templates/profile-delete-template.html')

    def test_delete_view_form_is_correct_type(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertIsInstance(form, ProfileDeleteForm)
