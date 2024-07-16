from django.urls import path
from .views import UserListView, UserDetailView, TaskListView
from .import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
]
