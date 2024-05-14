from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['assigned_by', 'status']

class MoveTaskForm(forms.Form):
    next_status = forms.ChoiceField(choices=[
        ('IN PROGRESS', 'Move to In Progress'),
        ('DONE', 'Move to Done'),
    ])