from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.contrib.auth import authenticate
from .models import Tool
from .forms import ToolUploadForm


def tool_list(request):
    tools = Tool.objects.all()
    return render(request, 'store/tool_list.html', {'tools': tools})


def tool_detail(request, pk):
    tool = get_object_or_404(Tool, pk=pk)
    return render(request, 'store/tool_detail.html', {'tool': tool})


def tool_download(request, pk):
    tool = get_object_or_404(Tool, pk=pk)
    tool.downloads += 1
    tool.save()
    return FileResponse(tool.file.open(), as_attachment=True, filename=tool.file.name.split('/')[-1])


def tool_upload(request):
    if request.method == 'POST':
        form = ToolUploadForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                tool = Tool(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    version=form.cleaned_data['version'],
                    file=request.FILES['file']
                )
                tool.save()
                return redirect('tool_list')
            else:
                error_message = '用户名或密码错误，或无上传权限'
                return render(request, 'store/tool_upload.html', {'form': form, 'error_message': error_message})
        else:
            return render(request, 'store/tool_upload.html', {'form': form})
    else:
        form = ToolUploadForm()
        return render(request, 'store/tool_upload.html', {'form': form})
