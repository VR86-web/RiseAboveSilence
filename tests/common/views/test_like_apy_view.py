from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from RiseAboveSilence.common.models import Like
from RiseAboveSilence.posts.models import Post

User = get_user_model()


class ToggleLikeAPITest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        # Create a post
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            user=self.user  # required if Post.user is NOT NULL
        )
        # API client
        self.client = APIClient()
        # URL for toggle like
        self.url = f'/api/posts/{self.post.pk}/like/'  # replace with your actual URL path

    def test_like_post_creates_like(self):
        """POST request should like the post if not liked yet"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['liked'])
        self.assertEqual(response.data['like_count'], 1)
        self.assertTrue(Like.objects.filter(user=self.user, to_post=self.post).exists())

    def test_unlike_post_removes_like(self):
        """POST request should unlike if already liked"""
        # Create the like first
        Like.objects.create(user=self.user, to_post=self.post)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['liked'])
        self.assertEqual(response.data['like_count'], 0)
        self.assertFalse(Like.objects.filter(user=self.user, to_post=self.post).exists())

    def test_unauthenticated_user_cannot_like(self):
        """Anonymous users cannot like a post"""
        response = self.client.post(self.url)
        self.assertIn(response.status_code, [401, 403])



