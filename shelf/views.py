from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import User
from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import CommentForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username"]

@login_required
def index(request):
    return render(request, "shelf/index.html")

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if request.POST.get("invite_code") != settings.INVITE_CODE:
            form.add_error(None, "邀请码不对哦")
        elif form.is_valid():
            login(request, form.save())
            return redirect("index")
    return render(request, "shelf/register.html", {"form": form})


@login_required
def index(request):
    posts = Post.objects.filter(is_public=True).order_by("-created")
    return render(request, "shelf/index.html", {"posts": posts})

@login_required
def my_posts(request):
    posts = request.user.posts.order_by("-created")
    return render(request, "shelf/my_posts.html", {"posts": posts})

@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("my_posts")
    return render(request, "shelf/new_post.html", {"form": form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("my_posts")
    return render(request, "shelf/new_post.html", {"form": form, "editing": True})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
    return redirect("my_posts")

from .forms import CommentForm

@login_required
def index(request):
    posts = Post.objects.filter(is_public=True).order_by("-created").prefetch_related("comments")
    return render(request, "shelf/index.html", {"posts": posts, "comment_form": CommentForm()})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_public=True)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect("index")