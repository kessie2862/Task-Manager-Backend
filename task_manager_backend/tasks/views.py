from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, TaskSerializer
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView
from .models import Task


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required.'}, status=400)

            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()

            refresh = RefreshToken.for_user(user)

            return JsonResponse({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'Username taken. Choose another username.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=200)
        else:
            return JsonResponse({'error': 'Unable to login. Check username and password.'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Assign the authenticated user as the creator of the task
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Tasks created by the user
        created_tasks = Task.objects.filter(created_by=user)

        total_created_tasks = created_tasks.count()
        completed_created_tasks = created_tasks.filter(
            status='completed').count()
        in_progress_created_tasks = created_tasks.filter(
            status='in_progress').count()
        overdue_created_tasks = created_tasks.filter(
            due_date__lt=timezone.now(), status__in=['open', 'in_progress']).count()

        # Tasks assigned
        assigned_tasks = Task.objects.filter(assigned_user=user)

        total_assigned_tasks = assigned_tasks.count()
        completed_assigned_tasks = assigned_tasks.filter(
            status='completed').count()
        in_progress_assigned_tasks = assigned_tasks.filter(
            status='in_progress').count()
        overdue_assigned_tasks = assigned_tasks.filter(
            due_date__lt=timezone.now(), status__in=['open', 'in_progress']).count()
