from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskSerializer(serializers.ModelSerializer):
    assigned_user = UserSerializer(read_only=True)
    assigned_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='assigned_user')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date',
                  'status', 'assigned_user', 'assigned_user_id', 'created_by']
        read_only_fields = ['created_by']
