from django import forms

from RiseAboveSilence.accounts.mixins import DisableFieldsMixin
from RiseAboveSilence.posts.models import Post


class PostsBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = (
            "is_approved",
            "user",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter post title",
                }
            ),
            "content": forms.Textarea(
                attrs={"placeholder": "Write your post content here...", "rows": 5}
            ),
        }
        labels = {
            "title": "Post Title",
            "content": "Post Content",
        }
        error_messages = {
            "title": {
                "required": "Title cannot be empty.",
                "max_length": "Title is too long.",
            },
            "content": {
                "required": "Content is required to create a post.",
            },
        }


class PostCreateForm(PostsBaseForm):
    pass


class PostUpdateForm(PostsBaseForm):
    pass


class PostDeleteForm(PostsBaseForm, DisableFieldsMixin):
    disabled_fields = ("__all__",)
