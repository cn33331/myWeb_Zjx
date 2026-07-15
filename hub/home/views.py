from django.shortcuts import render
from django.urls import reverse


def index(request):
    """平台首页：展示各功能模块入口。

    Returns:
        HttpResponse: 渲染 home/index.html，上下文包含 modules 列表，
            每个模块含 code(标识)、name(中文名)、desc(描述)、url(入口地址)。
    """
    modules = [
        {
            'code': 'STORE',
            'name': '应用商店',
            'desc': '浏览、上传与下载工具应用',
            'url': reverse('tool_list'),
        },
        {
            'code': 'FORUM',
            'name': '论坛',
            'desc': '发帖讨论与分享交流',
            'url': reverse('forum_home'),
        },
    ]
    return render(request, 'home/index.html', {'modules': modules})
