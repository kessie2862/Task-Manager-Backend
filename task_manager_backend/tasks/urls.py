from django.urls import path
from .views import UserListView, UserDetailView, TaskListView, TaskDetailView, TaskSummaryView
from .import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/summary/', TaskSummaryView.as_view(), name='task-summary'),
]
