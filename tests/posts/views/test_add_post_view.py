from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from RiseAboveSilence.posts.models import Post

User = get_user_model()


class AddPostViewIntegrationTests(TestCase):
    def setUp(self):
        # Create and log in a user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        # URL for creating posts
        self.url = reverse("add-post")  # adjust the name if different

        # Valid post data
        self.post_data = {
            "title": "Test Post",
            "content": "This is a test post.",
        }

    def test_post_creation_creates_new_post(self):
        response = self.client.post(self.url, data=self.post_data)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_user_is_set_correctly(self):
        self.client.post(self.url, data=self.post_data)
        post = Post.objects.first()
        self.assertEqual(post.user, self.user)

    def test_redirects_to_all_posts_after_creation(self):
        response = self.client.post(self.url, data=self.post_data)
        self.assertRedirects(response, reverse("all-posts"))

    def test_logged_out_user_redirected_to_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")
