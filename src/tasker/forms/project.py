from django import forms
from django.forms import formset_factory
from tasker.models import Project, User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'title',
            'description',
        )

        labels = {
            'title': 'Название',
            'description': 'Описание',
        }

        widgets = {
            'title' : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите название',
                }
            ),

            'description' : forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите описание',
                }
            )
        }


class MemberForm(forms.Form):
    username = forms.CharField(
        label='Участник',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите участника',
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            return username

        raise forms.ValidationError('Пользователя {} не существует'.format(username))


MemberFormset = formset_factory(MemberForm, extra=1)
