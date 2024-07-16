from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken


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
