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
