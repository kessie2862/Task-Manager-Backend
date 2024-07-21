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
                  'status', 'priority', 'assigned_user', 'assigned_user_id', 'created_by']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        assigned_user = validated_data.pop('assigned_user')
        task = Task.objects.create(
            assigned_user=assigned_user, **validated_data)
        return task

    def update(self, instance, validated_data):
        assigned_user = validated_data.pop('assigned_user', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        if assigned_user:
            instance.assigned_user = assigned_user
        instance.save()
        return instance
