from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.postgres.search import TrigramSimilarity
from tasker.models import Project, Task


@method_decorator(login_required, name='dispatch')
class SearchListView(ListView):
    def dispatch(self, request, *args, **kwargs):
        prev_request = request.META['HTTP_REFERER'] 
        query = request.GET.get('search').strip()
        if not query:
            return redirect(prev_request)
        
        projects = Project.own.all(user=request.user).annotate(
            similarity=TrigramSimilarity('title', query),
        ).filter(similarity__gt=0.3).order_by('-similarity')

        tasks = Task.objects.filter(
            Q(performer=request.user) | Q(author=request.user)
        ).annotate(
            similarity=TrigramSimilarity('title', query),
        ).filter(similarity__gt=0.3).order_by('-similarity')

        # projects = Project.own.all(user=request.user).filter(
        #     title__icontains=query
        # )

        # tasks = Task.objects.filter(
        #     Q(performer=request.user) | Q(author=request.user),
        #     Q(title__icontains=query)
        # )
        
        return render(request, 'inc/search.html', {
            'projects': projects,
            'tasks': tasks,
            'info': query,
        })
