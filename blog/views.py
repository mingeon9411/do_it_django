from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import PostForm

# Create your views here.
class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    ordering = '-pk'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# def index(request):
#     posts = Post.objects.all().order_by('-pk')

#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)

#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )