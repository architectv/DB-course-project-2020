from django.db import models
from .user import User
from tasker.managers import ProjectManager


class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=256, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    members = models.ManyToManyField(User, related_name='projects')

    date = models.DateTimeField(auto_now_add=True)
    tasks_number = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    own = ProjectManager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)
    
    def members_choices(self):
        members = self.members.all()
        members = [(m.id, m.username) for m in members]
        return members
    
    def add_member(self, member):
        self.members.add(member)
        self.save()
    
    def save_formset(self, formset):
        self.add_member(self.author)
        for form in formset:
            member_username = form.cleaned_data.get('username')
            if member_username:
                member = User.objects.get(username=member_username)
                self.add_member(member)
    
    def update(self, form, formset):
        new_project = form.save(commit=False)

        self.title = new_project.title
        self.description = new_project.description
        self.save()

        self.save_formset(formset)
