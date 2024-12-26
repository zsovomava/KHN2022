from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CommentForm, VideochatCodeForm
from .models import Comment, Post, Tip, Topic


def home(request):
    tip = Tip.get_a_tip()
    return render(request, 'main/home.html', context={'tip': tip})


class PostListView(ListView):
    model = Post
    ordering = ['-pub_date']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'main/user_post_list.html'
    ordering = ['-pub_date']
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        return context


class TopicPostListView(ListView):
    model = Post
    template_name = 'main/topic_post_list.html'
    ordering = ['-pub_date']
    paginate_by = 3

    def get_queryset(self):
        topic = get_object_or_404(Topic, name=self.kwargs.get('topic'))
        return Post.objects.filter(topic=topic)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.kwargs.get('topic')
        return context


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    return render(request, 'main/post_detail.html', context={'object': post, 'form': form})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'topic', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'topic', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff and not post.author.is_superuser


@login_required
def comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = post
            form.save()
            messages.success(request, 'Komment létrehozva.')
    return redirect('main:post-detail', pk=pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('main:post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_staff and not (comment.author and comment.author.is_superuser)


def videochat(request):
    if request.method == 'POST':
        form = VideochatCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            return redirect('main:jitsi', code)
    else:
        form = VideochatCodeForm()
    return render(request, 'main/videochat.html', context={'form': form})


def jitsi(request, room):
    return render(request, 'main/jitsi.html', context={'room': room, 'email': request.user.email, 'username': request.user.username})
