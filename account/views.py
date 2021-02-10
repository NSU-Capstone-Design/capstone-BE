from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserLoginSerializer, UserCreateSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error.", "code": 0}, status=status.HTTP_409_CONFLICT)

        check_id = User.objects.filter(user_id=serializer.validated_data['user_id']).first()
        check_email = User.objects.filter(email=serializer.validated_data['email']).first()
        if check_id is None and check_email is None:
            serializer.save()
            return Response({"message": "ok", "code": 1}, status=status.HTTP_201_CREATED)
        if check_id is not None:
            return Response({"message": "duplicate ID", "code": 2}, status=status.HTTP_409_CONFLICT)
        if check_email is not None:
            return Response({"message": "duplicate Email", "code": 3}, status=status.HTTP_409_CONFLICT)


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
            'user_id': serializer.data['user_id'],
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)
