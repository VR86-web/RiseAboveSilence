from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Post(models.Model):

    title = models.CharField(
        max_length=100,
    )

    content = models.TextField()

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    is_approved = models.BooleanField(
        default=False,
    )

    class Meta:
        permissions = [
            ("can_approve_post", "Can approve posts"),
        ]

    def __str__(self):
        return self.title
