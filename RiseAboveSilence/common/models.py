from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

from RiseAboveSilence.posts.models import Post

UserModel = get_user_model()


class News(models.Model):
    title = models.CharField(
        max_length=200,
    )
    content = models.TextField()

    image = CloudinaryField(
        'profile_picture',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return f"Comment by {self.user} on {self.to_post.title}"


class Like(models.Model):
    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )
