from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_task, name='add_task'),
    path('allTasks', views.view_tasks, name='view_tasks'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('complete/<int:task_id>/', views.mark_task_completed, name='mark_task_completed'),
]
