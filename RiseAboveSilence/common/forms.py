from django import forms

from RiseAboveSilence.common.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

        labels = {
            "content": "",
        }

        error_messages = {
            "content": {
                "required": "Content is required. Write it!",
            },
        }

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Write your comment...",
                }
            ),
        }
