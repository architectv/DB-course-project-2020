from django.db import models


class TaskManager(models.Manager):
    def assigned(self, performer):
        return self.filter(
            performer=performer,
        )
    
    def created(self, author):
        return self.filter(
            author=author,
        )
    
    def form_save(self, request, project, form):
        task = form.save(commit=False)
        task.author = request.user
        task.project = project
        task.save()

        task.add_tags(form.cleaned_data['tags'])
        
        return task
    
    def member_delete(self, project, member):
        created_tasks = self.created(author=member).filter(project=project)
        for task in created_tasks:
            task.delete()

        assigned_tasks = self.assigned(performer=member).filter(project=project)
        for task in assigned_tasks:
            task.performer = task.author
            task.save()
