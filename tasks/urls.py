from django.urls import path
from . import views


urlpatterns = [
    path('task_list/', views.task_list, name='task_list'),
    path('task_detail/<int:task_id>/',views.task_detail, name="task_detail"),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('update-status/<int:task_id>/', views.update_status, name='update_status'),
]
