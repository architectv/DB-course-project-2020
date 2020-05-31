from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tasker.models import User, Project, Task, Tag
from django.contrib import messages
from django.utils.http import is_safe_url, urlunquote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from tasker.forms import TaskForm, TaskStatusForm
from .pagination import *
from .decorators import *


@method_decorator(login_required, name='dispatch')
class InboxView(ListView):
    model = Task
    template_name = 'task/inbox.html'

    def get_context_data(self, **kwargs):
        context = super(InboxView, self).get_context_data(**kwargs) 
        tasks = Task.own.assigned(performer=self.request.user)
        tasks, _ = PaginationView.paginate(self.request, tasks)

        context['tasks'] = tasks

        return context


@method_decorator(task_member_decorators, name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'

    def dispatch(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        info = task.get_info()        
        tags = task.tags.all()

        if request.method == 'POST':
            form = TaskStatusForm(request.POST)
        else:
            form = TaskStatusForm()
        
        return render(request, 'task/show_task.html', {
            'task':task,
            'form':form,
            'info':info,
            'tags':tags,
        })


@method_decorator(project_member_decorators, name='dispatch')
class TaskCreateView(CreateView):
    def dispatch(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        members = project.members_choices()

        form = TaskForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                task = Task.own.form_save(request, project, form)
                return redirect('show_task', task.id)
        else:
            form.fields['performer'].choices = members

        return render(request, 'task/new_task.html', {
            'form':form,
            'project':project,
        })


@method_decorator(task_performer_decorators, name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskStatusForm
    context_object_name = 'task'

    def dispatch(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)

        if request.user == task.performer:
            form = TaskStatusForm(request.POST)
            
            if form.is_valid():
                task.update_by_performer(request)

        return redirect('show_task', task_id)


@method_decorator(task_author_decorators, name='dispatch')
class TaskEditView(UpdateView):
    def dispatch(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        project = task.project
        members = project.members.all()
        members = [(m.id, m.username) for m in members]
        
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                prev_performer = task.performer
                task.update_by_author(request, form)
                if prev_performer != task.performer:
                    task.status = 'todo'
                    task.save()

                return redirect('show_task', task.id)
        else:
            form = TaskForm(instance=task)
            form.fields['performer'].choices = members
        
        return render(request, 'task/edit_task.html', {
            'form': form,
            'project': project,
            'task': task,
        })


@method_decorator(task_author_decorators, name='dispatch')
class TaskDeleteView(DeleteView):
    def dispatch(self, request, task_id, *args, **kwargs):
        task = Task.objects.get(id=task_id)
        project = task.project
        task.delete()
        
        return redirect('show_project', project.id)


@method_decorator(login_required, name='dispatch')
class InboxStatusView(ListView):
    def dispatch(self, request, status, *args, **kwargs):
        # tasks = Task.objects.filter(performer=request.user, status=status)
        tasks = Task.own.assigned(performer=request.user).filter(status=status)
        tasks, _ = PaginationView.paginate(self.request, tasks)

        return render(request, 'task/inbox.html', {
            'tasks': tasks,
            'info': status,
        })


@method_decorator(login_required, name='dispatch')
class InboxTagView(ListView):
    def dispatch(self, request, tag_id, *args, **kwargs):
        tag = Tag.objects.get(id=tag_id)
        # tasks = Task.objects.filter(performer=request.user, tags=tag)
        tasks = Task.own.assigned(performer=request.user).filter(tags=tag)
        tasks, _ = PaginationView.paginate(self.request, tasks)
        
        return render(request, 'task/inbox.html', {
            'tasks': tasks,
            'info': tag,
        })
    