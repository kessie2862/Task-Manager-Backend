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

            refresh = RefreshToken.for_user(user)

            return JsonResponse({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'Username taken. Choose another username.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
