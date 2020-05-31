from django import forms
from tasker.models import Task


class TaskStatusForm(forms.Form):
    status = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices=Task.STATUS_CHOICES,
        initial='todo',
    )


class TaskForm(forms.ModelForm):
    upto = forms.DateTimeField(
        required=False,
        input_formats = ['%Y-%m-%dT%H:%M'],
        label='Срок',
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
                },
            format='%Y-%m-%dT%H:%M')
    )

    tags = forms.CharField(
        required=False,
        label='Теги',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите теги через пробел',
                },)
    )

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'performer',
            'upto',
        )

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'performer': 'Исполнитель',
            'upto': 'Срок',
        }

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите название',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите описание',
                }
            ),

            'performer': forms.Select(attrs={'class': 'form-control'}),
        }
