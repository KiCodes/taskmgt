from . import views
from django.urls import path

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskPageView.as_view(),name='index'),
    path('add_task', views.AddTaskPageView.as_view(),name='add_task'),
    path('move_task/<pk>', views.MoveTask.as_view(), name='move_task')
]