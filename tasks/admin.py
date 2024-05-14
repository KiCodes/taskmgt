from django.contrib import admin
from .models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category', 'status', 'assigned_to')
    list_filter = ('category', 'status')

admin.site.register(Task, TaskAdmin)