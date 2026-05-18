from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post, Category, Tag
from .forms import PostForm, CommentForm


class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(post_count=Count('post'))
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(post_count=Count('post'))
        context['comments'] = self.object.comment_set.order_by('created_at')
        context['comment_form'] = CommentForm()
        return context

    def post(self, request):
        post = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
        return redirect(post.get_absolute_url())


class PostListByCategory(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    ordering = '-pk'

    def get_queryset(self):
        slug = self.kwargs['slug']
        if slug == 'no_category':
            return Post.objects.filter(category=None).order_by('-pk')
        category = Category.objects.get(slug=slug)
        return Post.objects.filter(category=category).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['categories'] = Category.objects.annotate(post_count=Count('post'))
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        if slug == 'no_category':
            context['category'] = '미분류'
        else:
            context['category'] = Category.objects.get(slug=slug)
        return context


class PostListByTag(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    ordering = '-pk'

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(tags=tag).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(post_count=Count('post'))
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})
