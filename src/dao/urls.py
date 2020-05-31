"""dao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from tasker.views import *
from tasker import views
from tasker.forms import UserLoginForm
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit/', UserEditView.as_view(), name='edit'),
    path('', ProjectListView.as_view(), name='index'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('project/<int:project_id>/', ProjectDetailView.as_view(), name='show_project'),
    path('project/new/', ProjectCreateView.as_view(), name='create_project'),
    path('project/<int:project_id>/edit/', ProjectUpdateView.as_view(), name='edit_project'),
    path('project/<int:project_id>/remove/', ProjectDeleteView.as_view(), name='delete_project'),
    path('project/<int:project_id>/del/<int:member_id>/', ProjectDeleteMemberView.as_view(), name='delete_member'),
    path('project/<int:project_id>/out/', ProjectOutView.as_view(), name='out_project'),
    path('task/<int:task_id>/', TaskDetailView.as_view(), name='show_task'),
    path('project/<int:project_id>/add/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:task_id>/edit/', TaskEditView.as_view(), name='edit_task'),
    path('task/<int:task_id>/update/', TaskUpdateView.as_view(), name='update_task'),
    path('task/<int:task_id>/remove/', TaskDeleteView.as_view(), name='delete_task'),
    path('project/<int:project_id>/status/<slug:status>/', ProjectStatusView.as_view(), name='project_filter'),
    path('project/<int:project_id>/tag/<int:tag_id>/', ProjectTagView.as_view(), name='project_tasks_by_tag'),
    path('inbox/status/<slug:status>/', InboxStatusView.as_view(), name='inbox_filter'),
    path('inbox/tag/<int:tag_id>/', InboxTagView.as_view(), name='tasks_by_tag'),
    path('search/', SearchListView.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
