from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
import jwt
from django.conf import settings
# from .models import User
# from .serializers import UserSerializer, UserCreateSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_posts(request):
    if request.method != 'GET':
        return

    return Response({"message": "ok", "code": 1}, status=status.HTTP_201_CREATED)
