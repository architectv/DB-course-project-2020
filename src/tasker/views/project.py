from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from tasker.models import User, Project, Task, Tag
from tasker.forms import ProjectForm, MemberFormset
from .pagination import *
from .decorators import *


class ProjectListView(ListView):
    model = Project
    template_name = 'project/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            projects = Project.own.all(self.request.user)
            projects, _ = PaginationView.paginate(self.request, projects)
            context['projects'] = projects

        return context


@method_decorator(project_member_decorators, name='dispatch')
class ProjectDetailView(DetailView):
    def dispatch(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        tasks = Task.objects.filter(project__id=project_id)
        tasks, _ = PaginationView.paginate(self.request, tasks)

        return render(request, 'project/show_project.html', {
            'project': project,
            'tasks': tasks,
        })


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    template_name = 'project/new_project.html'

    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        formset = MemberFormset()

        return self.render_to_response({
            'form': form,
            'formset': formset,
        })
    
    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)
        formset = MemberFormset(request.POST)

        if form.is_valid() and formset.is_valid():
            project = Project.own.form_save(request, form, formset)
            return redirect('show_project', project.id)
        else:
            messages.error(request, 'Добавляемого пользователя не существует')
        
        return self.render_to_response({
            'form': form,
            'formset': formset,
        })


@method_decorator(project_author_decorators, name='dispatch')
class ProjectUpdateView(UpdateView):
    template_name = 'project/edit_project.html'

    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        formset = MemberFormset()
        form = ProjectForm(instance=project)

        return self.render_to_response({
            'form': form,
            'new_formset': formset,
            'project': project,
        })
    
    def post(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        formset = MemberFormset(request.POST)
        form = ProjectForm(request.POST)

        if form.is_valid() and formset.is_valid():
            project.update(form, formset)
            return redirect('show_project', project_id)
        else:
            messages.error(request, 'Добавляемого пользователя не существует')
        
        return self.render_to_response({
            'form': form,
            'new_formset': formset,
            'project':project,
        })


@method_decorator(project_author_decorators, name='dispatch')
class ProjectDeleteView(DeleteView):
    def dispatch(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        project.delete()
        return redirect('index')


# @method_decorator(project_member_decorators, name='dispatch')
# class ProjectDeleteMemberView(DeleteView):
#     def dispatch(self, request, project_id, member_id, *args, **kwargs):
#         project = Project.objects.get(id=project_id)
#         member = project.members.get(id=member_id)

#         if member == project.author:
#             return redirect('index')
#         elif request.method == 'POST':
#             Task.own.member_delete(project, member)
#             project.members.remove(member)
            
#             if request.user != member:
#                 return redirect('show_project', project_id)
#             else:
#                 return redirect('index')
#         elif request.user == member:
#             return render(request, 'project/out_project.html', {
#                 'project': project,
#             })


#         return render(request, 'project/delete_member.html', {
#             'project': project,
#             'member': member,
#         })


@method_decorator(project_author_decorators, name='dispatch')
class ProjectDeleteMemberView(DeleteView):
    def dispatch(self, request, project_id, member_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        member = project.members.get(id=member_id)
        if member == project.author:
            return redirect('index')
        
        if request.method == 'POST':
            Task.own.member_delete(project, member)
            project.members.remove(member)
            return redirect('show_project', project_id)

        return render(request, 'project/delete_member.html', {
            'project': project,
            'member': member,
        })


@method_decorator(project_member_decorators, name='dispatch')
class ProjectOutView(DeleteView):
    def dispatch(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        if request.user == project.author:
            return redirect('index')

        if request.method == 'POST':
            Task.own.member_delete(project, request.user)
            project.members.remove(request.user)
            return redirect('index')

        return render(request, 'project/out_project.html', {
            'project': project,
        })


@method_decorator(project_member_decorators, name='dispatch')
class ProjectStatusView(ListView):
    def dispatch(self, request, project_id, status, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        tasks = Task.objects.filter(project__id=project_id, status=status)
        tasks, _ = PaginationView.paginate(self.request, tasks)

        return render(request, 'project/show_project.html', {
            'project': project,
            'tasks': tasks,
            'info': status,
        })


@method_decorator(project_member_decorators, name='dispatch')
class ProjectTagView(ListView):
    def dispatch(self, request, project_id, tag_id, *args, **kwargs):
        project = Project.objects.get(id=project_id)
        tag = Tag.objects.get(id=tag_id)
        tasks = Task.objects.filter(project=project, tags=tag)
        tasks, _ = PaginationView.paginate(self.request, tasks)

        return render(request, 'project/show_project.html', {
            'project': project,
            'tasks': tasks,
            'tag': tag,
        })
