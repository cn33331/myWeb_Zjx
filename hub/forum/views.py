from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from .models import ForumUser, Topic, Post
from .forms import RegisterForm, LoginForm, TopicForm, PostForm


def get_current_user(request):
    """获取当前登录用户身份，返回 (user, is_admin)。

    admin 用户首次发帖时自动创建对应的 ForumUser（is_approved=True），
    普通用户从 session 中的 forum_user_id 获取。
    """
    if request.session.get('is_admin'):
        admin_username = request.session.get('admin_username', 'admin')
        user, _ = ForumUser.objects.get_or_create(
            username=admin_username,
            defaults={'is_approved': True, 'password': 'admin-managed'}
        )
        return user, True
    if 'forum_user_id' in request.session:
        user = ForumUser.objects.filter(pk=request.session['forum_user_id']).first()
        return user, False
    return None, False


def admin_required(view_func):
    """仅允许 Django admin 用户访问。"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            return redirect('forum_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_required(view_func):
    """允许 admin 用户或已登录的论坛用户访问。"""
    def wrapper(request, *args, **kwargs):
        if 'forum_user_id' not in request.session and not request.session.get('is_admin'):
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 优先检查 Django admin 用户
            django_user = authenticate(request, username=username, password=password)
            if django_user is not None and django_user.is_staff:
                request.session['is_admin'] = True
                request.session['admin_username'] = username
                return redirect('forum_home')

            # 检查论坛用户
            user = ForumUser.objects.filter(username=username).first()
            if user and check_password(password, user.password):
                if user.is_approved:
                    request.session['forum_user_id'] = user.pk
                    return redirect('forum_home')
                else:
                    return render(request, 'forum/login.html', {
                        'form': form,
                        'error_message': '账号尚未通过审核，请等待管理员审核'
                    })
            else:
                return render(request, 'forum/login.html', {
                    'form': form,
                    'error_message': '用户名或密码错误'
                })
    else:
        form = LoginForm()
    return render(request, 'forum/login.html', {'form': form})


def forum_logout(request):
    request.session.pop('forum_user_id', None)
    request.session.pop('is_admin', None)
    request.session.pop('admin_username', None)
    return redirect('forum_home')


def forum_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if ForumUser.objects.filter(username=username).exists():
                return render(request, 'forum/register.html', {
                    'form': form,
                    'error_message': '用户名已存在'
                })
            hashed_password = make_password(form.cleaned_data['password'])
            ForumUser.objects.create(
                username=username,
                password=hashed_password,
                email=email
            )
            return render(request, 'forum/register_success.html')
    else:
        form = RegisterForm()
    return render(request, 'forum/register.html', {'form': form})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.views += 1
    topic.save()
    posts = Post.objects.filter(topic=topic)

    user, is_admin = get_current_user(request)

    if request.method == 'POST' and user and user.is_approved:
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
    if not user or not user.is_approved:
        return render(request, 'forum/not_approved.html')

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


@admin_required
def admin_review(request):
    pending_users = ForumUser.objects.filter(is_approved=False)
    approved_users = ForumUser.objects.filter(is_approved=True)

    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        if action == 'approve' and user_id:
            user = get_object_or_404(ForumUser, pk=user_id)
            user.is_approved = True
            user.approved_date = timezone.now()
            user.save()
        elif action == 'reject' and user_id:
            user = get_object_or_404(ForumUser, pk=user_id)
            user.delete()

    return render(request, 'forum/admin_review.html', {
        'pending_users': pending_users,
        'approved_users': approved_users
    })
