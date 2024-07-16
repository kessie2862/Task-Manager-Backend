from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ])
    assigned_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_tasks', default=1)

    def __str__(self):
        return self.title
