from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model

from RiseAboveSilence.accounts.models import Profile

User = get_user_model()


class UserSignalTest(TestCase):
    def test_profile_created_and_welcome_email_sent(self):
        # Clear mailbox
        mail.outbox = []

        # Create a user (this triggers the signal)
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

        # Check that a Profile was created
        profile_exists = Profile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists)

        # Check that one email was sent
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, 'Welcome to Rise Above Silence!')
        self.assertIn('Thanks for joining our community', sent_email.body)
        self.assertEqual(sent_email.to, ['testuser@example.com'])
