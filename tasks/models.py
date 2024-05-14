from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status_choices = [
        ('TO DO', 'To Do'),
        ('IN PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    category_choices = [
        ('WORK', 'Work'),
        ('PERSONAL', 'Personal'),
        ('OTHERS', 'Others'),
    ]
    category = models.CharField(max_length=20, choices=category_choices, default='PERSONAL')
    status = models.CharField(max_length=20, choices=status_choices, default='TO DO')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    def __str__(self):
        return self.title
    




