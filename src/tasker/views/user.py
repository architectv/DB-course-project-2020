from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView
from django.contrib.auth import views as auth_views
from tasker.models import *
from tasker.forms import *
from .pagination import *
from .decorators import *


@method_decorator(logout_only, name='dispatch')
class LoginView(auth_views.LoginView):
    pass


@method_decorator(logout_only, name='dispatch')
class RegisterView(CreateView):
    template_name = 'user/register.html'

    def get(self, request, *args, **kwargs):
        user_form = UserRegistrationForm()
        return self.render_to_response({'user_form': user_form})
    
    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'user/register_done.html', {
                'new_user': new_user,
            })

        return self.render_to_response({
            'user_form': user_form,
        })


@method_decorator(login_required, name='dispatch')
class UserEditView(UpdateView):
    model = User
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_form = UserEditForm(
                instance=request.user,
                data=request.POST,
                files=request.FILES)

            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Аккаунт успешно обновлен')
            else:
                messages.error(request, 'Ошибка обновления аккаунта')
        else:
            user_form = UserEditForm(instance=request.user)

        return render(request, 'user/edit.html', {
            'user_form': user_form,
        })
