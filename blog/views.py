from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Count, Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post, Category, Tag
from .forms import PostForm, CommentForm


def _apply_tags(post, tags_input):
    for tag_name in tags_input.split(','):
        tag_name = tag_name.strip()
        if tag_name:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)


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
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comments'] = self.object.comment_set.order_by('created_at')
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
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
        context['category'] = '미분류' if slug == 'no_category' else Category.objects.get(slug=slug)
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


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.user.is_authenticated:
            post.author = self.request.user
        post.save()
        _apply_tags(post, form.cleaned_data.get('tags_input', ''))
        return redirect(post.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['tags_input'] = ', '.join(self.object.tags.values_list('name', flat=True))
        return initial

    def form_valid(self, form):
        post = form.save()
        post.tags.clear()
        _apply_tags(post, form.cleaned_data.get('tags_input', ''))
        return redirect(post.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


def post_search(request):
    q = request.GET.get('q', '').strip()
    posts = Post.objects.filter(
        Q(title__icontains=q) | Q(content__icontains=q)
    ).order_by('-pk') if q else Post.objects.none()
    categories = Category.objects.annotate(post_count=Count('post'))
    return render(request, 'blog/post_list.html', {
        'object_list': posts,
        'categories': categories,
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'search_query': q,
    })


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
