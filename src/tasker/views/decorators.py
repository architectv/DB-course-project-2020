from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from functools import wraps
from tasker.models import User, Project, Task, Tag


def project_author_only(function):
    @wraps(function)
    def wrap(request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        if request.user == project.author:
            return function(request, project_id, *args, **kwargs)
        else:
            return redirect('index')
    return wrap


def project_member_only(function):
    @wraps(function)
    def wrap(request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        if request.user in project.members.all():
            return function(request, project_id, *args, **kwargs)
        else:
            return redirect('index')
    return wrap


def task_member_only(function):
    @wraps(function)
    def wrap(request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        if request.user in task.project.members.all():
            return function(request, task_id, *args, **kwargs)
        else:
            return redirect('index')
    return wrap


def task_author_only(function):
    @wraps(function)
    def wrap(request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        if request.user == task.author:
            return function(request, task_id, *args, **kwargs)
        else:
            return redirect('index')
    return wrap


def task_performer_only(function):
    @wraps(function)
    def wrap(request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        if request.user == task.performer:
            return function(request, task_id, *args, **kwargs)
        else:
            return redirect('index')
    return wrap


def logout_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap


task_member_decorators = [login_required, task_member_only]
task_performer_decorators = [login_required, task_performer_only]
task_author_decorators = [login_required, task_author_only]
project_member_decorators = [login_required, project_member_only]
project_author_decorators = [login_required, project_author_only]
