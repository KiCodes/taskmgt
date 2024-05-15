from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, FormView, View, DeleteView
from .models import Task
from .forms import MoveTaskForm, TaskForm
from django.urls import reverse_lazy

# Create your views here.
class TaskPageView(DetailView):
    template_name = 'tasks/index.html'

    def get_object(self):
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        tasks_todo = Task.objects.filter(assigned_to=user, status='TO DO')
        tasks_in_progress = Task.objects.filter(assigned_to=user, status='IN PROGRESS')
        tasks_done = Task.objects.filter(assigned_to=user, status='DONE')

        # Add tasks to context
        context['tasks_todo'] = tasks_todo
        context['tasks_in_progress'] = tasks_in_progress
        context['tasks_done'] = tasks_done
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # rerouting to the login page and attaching a 'next' parameter query to the url with the value of the url user tried to access
            return redirect(f"auth/login?next={request.path}")
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if 'delete_tasks' in request.POST:
            tasks_to_delete = request.POST.getlist('tasks_to_delete')
            Task.objects.filter(pk__in=tasks_to_delete).delete()
        return redirect('tasks:index')
    
class AddTaskPageView(FormView):
    template_name = 'tasks/add_task.html'
    form_class = TaskForm
    success_url = '/'

    def form_valid(self, form):
        # Create a new user with the data from the form
        form.instance.assigned_by = self.request.user
        form.save()
        return super().form_valid(form)

# View for handling moving tasks to the next status
class MoveTask(View):
    def post(self, request, *args, **kwargs):
        form = MoveTaskForm(request.POST)
        if form.is_valid():
            # Get the next status selected in the form
            next_status = form.cleaned_data['next_status']
             # Retrieve the task ID from URL kwargs
            task_id = kwargs.get('pk')
            # Retrieve the task object
            task = Task.objects.get(pk=task_id)
            # Update the task status to the selected next status
            task.status = next_status
            task.save()
        return redirect('tasks:index')  # Redirect to tasks:index view after updating the task status
    
class DeleteDoneTask(DeleteView):
    model = Task
        # template_name = 'tasks/delete_done_tasks.html'  # Create a template for confirmation if needed
    success_url = reverse_lazy('tasks:index')  # Redirect to the task list page after deletion
    def post(self, request, *args, **kwargs):
        # Check if the form was submitted for deleting task
        if 'delete_tasks' in request.POST:
        # Retrieve the list of selected task IDs to delete                
            tasks_to_delete_ids = request.POST.getlist('tasks_to_delete')
                # Delete the selected tasks
            Task.objects.filter(pk__in=tasks_to_delete_ids).delete()

            # Redirect to the success URL after deletion
        return redirect(self.success_url)
    