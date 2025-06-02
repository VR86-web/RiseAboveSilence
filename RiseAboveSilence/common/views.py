
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView

from RiseAboveSilence.common.forms import CommentForm
from RiseAboveSilence.common.models import News, Comment, Like
from RiseAboveSilence.posts.models import Post


class HomePage(ListView):
    model = News
    template_name = 'common_templates/index.html'
    paginate_by = 3
    context_object_name = 'news_items'


class AboutView(TemplateView):
    template_name = 'common_templates/about.html'


def comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_post = post
            comment.user = request.user
            comment.save()
            return redirect('details-post', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'posts_templates/all-post.html', {'post': post, 'form': form})


@login_required
def reply_to_comment(request, pk, comment_id):
    post = get_object_or_404(Post, pk=pk)
    parent_comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                to_post=post,
                user=request.user,
                content=content,
                parent=parent_comment
            )
        return redirect('details-post', pk=post.pk)

    return redirect('details-post', pk=post.pk)


@login_required
def likes_functionality(request, pk: int):
    liked_object = Like.objects.filter(
        to_post_id=pk,
        user=request.user
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_post_id=pk, user=request.user)
        like.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{pk}')

