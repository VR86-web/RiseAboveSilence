import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from django.views.decorators.http import require_GET
from django.views.generic import ListView, TemplateView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from RiseAboveSilence.common.forms import CommentForm
from RiseAboveSilence.common.models import News, Comment, Like
from RiseAboveSilence.posts.models import Post


class HomePage(ListView):
    model = News
    template_name = "common_templates/index.html"
    paginate_by = 3
    context_object_name = "news_items"


class AboutView(TemplateView):
    template_name = "common_templates/about.html"


def comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_post = post
            comment.user = request.user
            comment.save()
            return redirect("details-post", pk=pk)
    else:
        form = CommentForm()

    return render(
        request, "posts_templates/all-post.html", {"post": post, "form": form}
    )


logger = logging.getLogger(__name__)


@require_GET
@login_required
def async_new_comments(request):
    user = request.user
    since_str = request.GET.get("since")

    try:
        since = datetime.datetime.fromisoformat(since_str)
        if since.tzinfo is None:
            since = since.replace(tzinfo=datetime.timezone.utc)
    except (TypeError, ValueError):
        logger.warning("Invalid 'since' parameter: %s", since_str)
        since = now() - datetime.timedelta(minutes=5)

    post_comments = (
        Comment.objects.filter(
            to_post__user=user, created_at__gt=since, parent__isnull=True
        )
        .exclude(user=user)
        .select_related("user", "to_post")
    )

    reply_comments = (
        Comment.objects.filter(parent__user=user, created_at__gt=since)
        .exclude(user=user)
        .select_related("user", "to_post", "parent")
    )

    comments = sorted(
        list(post_comments) + list(reply_comments),
        key=lambda c: c.created_at,
        reverse=True,
    )

    data = []
    for comment in comments:
        data.append(
            {
                "id": comment.id,
                "type": "reply" if comment.parent else "post_comment",
                "content": comment.content[:80],
                "author": comment.user.username,
                "post_id": comment.to_post.id,
                "post_title": comment.to_post.title[:80],
            }
        )

    return JsonResponse(
        {
            "new_count": len(data),
            "notifications": data,
        }
    )


@login_required
def reply_to_comment(request, pk, comment_id):
    post = get_object_or_404(Post, pk=pk)
    parent_comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Comment.objects.create(
                to_post=post, user=request.user, content=content, parent=parent_comment
            )
        return redirect("details-post", pk=post.pk)

    return redirect("details-post", pk=post.pk)


class ToggleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, to_post=post)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        like_count = Like.objects.filter(to_post=post).count()
        return Response(
            {"liked": liked, "like_count": like_count}, status=status.HTTP_200_OK
        )
