from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .project import Project
from .user import User
from .tag import Tag
from tasker.managers import TaskManager


class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'Todo'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    )

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    date = models.DateTimeField(auto_now_add=True)
    upto = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    tags = models.ManyToManyField(Tag, blank=True)

    objects = models.Manager()
    own = TaskManager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)
    
    def get_info(self):
        info = {'text':"Без срока", 'state':'secondary'}

        if self.upto is not None:
            interval = self.upto - datetime.now(timezone.utc)
            if interval < timedelta(seconds=0):
                info['text'] = "Срок истек"
                info['state'] = 'danger'
            elif interval < timedelta(hours=1):
                info['text'] = "До конца менее 1 часа"
                info['state'] = 'warning'
            elif interval < timedelta(days=1):
                info['text'] = "До конца менее 24 часов"
                info['state'] = 'warning'
            else:
                info['text'] = "Срок истекает не скоро"
                info['state'] = 'secondary'
            
            if self.status == 'done':
                info['state'] = 'success'
        
        return info

    def add_tags(self, tags_string):
        tag_list = tags_string.split()
        for label in tag_list:
            tag, _ = Tag.objects.get_or_create(name=label)
            self.tags.add(tag)

    def update_by_performer(self, request):
        self.status = request.POST.get('status')
        self.add_tags(request.POST.get('tags'))
        self.save()
    
    def update_by_author(self, request, form):
        upd_task = form.save(commit=False)
        self.title = upd_task.title
        self.description = upd_task.description
        self.upto = upd_task.upto
        self.performer = upd_task.performer
        self.add_tags(form.cleaned_data['tags'])
        self.save()


@receiver(post_save, sender=Task)
def inc_project_tasks_number(sender, instance, created, **kwargs):
    if created:
        instance.project.tasks_number += 1
        instance.project.save()


@receiver(pre_delete, sender=Task)
def dec_project_tasks_number(sender, instance, **kwargs):
    instance.project.tasks_number -= 1
    instance.project.save()
