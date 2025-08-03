from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CustomUserRegisterViewIntegrationTests(TestCase):
    def setUp(self):
        # Common POST data for all tests
        self.post_data = {
            "username": "testuser",
            "email": "test@example.com",  # <-- required if your form needs it
            "password1": "SuperSecretPass123",
            "password2": "SuperSecretPass123",
        }

        self.register_url = reverse('register')
        self.index_url = reverse('index')

    def test_register_creates_user(self):
        self.client.post(self.register_url, data=self.post_data)
        self.assertTrue(UserModel.objects.filter(username='testuser').exists())

    def test_register_returns_redirect(self):
        response = self.client.post(self.register_url, data=self.post_data)
        self.assertEqual(response.status_code, 302)

    def test_register_redirects_to_index(self):
        response = self.client.post(self.register_url, data=self.post_data)
        self.assertEqual(response.url, self.index_url)