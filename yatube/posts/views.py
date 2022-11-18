from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from .forms import PostForm

from django.shortcuts import get_object_or_404, redirect, render

from .models import Group, Post, User



def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    template = 'posts/index.html'
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'posts': posts
    }
    return render(request, template, context)

def profile(request, username):
    author = get_object_or_404(User, username=username)
    all_posts = Post.objects.all().filter(author__username=username)
    counter = all_posts.count()
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    template = 'posts/profile.html'
    context = {
        'page': page,
        'author': author,
        'counter': counter
    } 

    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    template = 'posts/post_detail.html'
    context = {'post': post}

    return render(request, template, context)

@login_required(login_url="users:login")
def post_create(request):
    """Добавления поста."""

    template = "posts/create_post.html"

    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author_id = request.user.id
        instance.save()
        return redirect("posts:profile", request.user)

    return render(request, template, {"form": form})


@login_required(login_url="users:login")
def post_edit(request, post_id):
    """Редактирование поста. Доступно только автору."""

    template = "posts/create_post.html"

    post = get_object_or_404(Post, pk=post_id)

    # Если редактировать пытается не автор
    if request.user.id != post.author.id:
        return redirect("posts:post_detail", post.pk)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post.id)

    context = {
        "form": form,
        "is_edit": True,
    }
    return render(request, template, context)