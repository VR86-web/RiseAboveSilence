from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from RiseAboveSilence.common.forms import CommentForm
from RiseAboveSilence.posts.forms import PostCreateForm, PostUpdateForm, PostDeleteForm
from RiseAboveSilence.posts.models import Post


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts_templates/add-post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('all-posts')


class AllPostView(ListView):
    model = Post
    template_name = 'posts_templates/all-post.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    def get_queryset(self):
        return Post.objects.filter(is_approved=True).order_by('-created_at')


class DetailPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts_templates/detail-post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['is_creator'] = self.request.user == post.user
        context['form'] = CommentForm()
        context['comments'] = post.comments.filter(parent__isnull=True).order_by('-created_at')
        return context


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostUpdateForm
    model = Post
    template_name = 'posts_templates/update-post.html'

    def get_success_url(self):
        return reverse_lazy('details-post', kwargs={'pk': self.object.pk})

    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.request.user == post.user


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts_templates/delete-post.html'
    success_url = reverse_lazy('all-posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            context['form'] = PostDeleteForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user
