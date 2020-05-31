from django.db import models


class ProjectManager(models.Manager):
    def all(self, user):
        return self.filter(
            members=user,
        )
    
    def form_save(self, request, form, formset):
        project = form.save(commit=False)
        project.author = request.user
        project.save()

        project.save_formset(formset)
        return project
        