from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['assigned_by', 'status']

# Form for moving tasks to the next status
class MoveTaskForm(forms.Form):
    next_status = forms.ChoiceField(choices=[
        ('IN PROGRESS', 'Move to In Progress'),  # Choice to move task to 'In Progress' status
        ('DONE', 'Move to Done'),  # Choice to move task to 'Done' status
    ])

