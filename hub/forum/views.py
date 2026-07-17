from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Topic, Post
from .forms import TopicForm, PostForm


def get_current_user(request):
    if request.user.is_authenticated:
        return request.user, request.user.is_staff
    return None, False


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('forum_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def forum_home(request):
    topics = Topic.objects.all()
    user, is_admin = get_current_user(request)
    return render(request, 'forum/index.html', {
        'topics': topics,
        'user': user,
        'is_admin': is_admin,
    })


def forum_login(request):
    return redirect('/login/')


def forum_logout(request):
    return redirect('/')


def forum_register(request):
    return redirect('/register/')


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.views += 1
    topic.save()
    posts = Post.objects.filter(topic=topic)

    user, is_admin = get_current_user(request)

    if request.method == 'POST' and user:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = user
            post.save()
            return redirect('topic_detail', pk=pk)
    else:
        form = PostForm()

    return render(request, 'forum/topic_detail.html', {
        'topic': topic,
        'posts': posts,
        'user': user,
        'is_admin': is_admin,
        'form': form
    })


@login_required
def create_topic(request):
    user, is_admin = get_current_user(request)

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = user
            topic.save()
            return redirect('forum_home')
    else:
        form = TopicForm()
    return render(request, 'forum/create_topic.html', {
        'form': form,
        'user': user,
        'is_admin': is_admin,
    })


def admin_review(request):
    return redirect('/admin/')
