from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserLoginSerializer, UserCreateSerializer
from rest_framework.views import APIView
from django.contrib.auth.base_user import BaseUserManager
'''
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        check_id = User.objects.filter(user_id=serializer.validated_data['user_id']).first()
        check_email = User.objects.filter(email=serializer.validated_data['email']).first()
        if check_id is None and check_email is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        if check_id is not None:
            return Response({"message": "duplicate ID"}, status=status.HTTP_409_CONFLICT)
        if check_email is not None:
            return Response({"message": "duplicate Email"}, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['user_id'] == "None":
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)

        response = {
            'success': 'True',
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)
'''
#-------------------CBV----------------------------------------------------------
class UserManagerAPIView(APIView, BaseUserManager):
    def _create_user(self, request):
        """
        Creates and saves a User with the given email and password.
        """
        if not request.data.get['user_id']:
            raise ValueError('The given email must be set')

        user = User(
            user_id=request.data.get['user_id'],
            email=request.data.get['email'],
            nickname=request.data.get['nickname'],
            level=request.data.get['level'],
            expert_user=request.data.get['expert_user']
        )
        user.set_password(request.data.get['password'])
        user.save(using=self._db)
        return user

    def create_superuser(self, request):
        user = self._create_user(request)
        user.is_superuser = True  # 나중에 지우자
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserAPIVIEW(APIView):
    def create_user(self,request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        check_id = User.objects.filter(user_id=serializer.validated_data['user_id']).first()
        check_email = User.objects.filter(email=serializer.validated_data['email']).first()
        if check_id is None and check_email is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        if check_id is not None:
            return Response({"message": "duplicate ID"}, status=status.HTTP_409_CONFLICT)
        if check_email is not None:
            return Response({"message": "duplicate Email"}, status=status.HTTP_409_CONFLICT)

    def login(request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['user_id'] == "None":
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)

        response = {
            'success': 'True',
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)