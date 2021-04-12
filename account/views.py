from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings
from .models import User
import json
from .serializers import UserSerializer, UserCreateSerializer


# 인증이 필요한 요청 예제
class TestView(APIView):
    # 이부분 설정을 해주면 토큰으로 유저가 맞는지 확인 합니다.(유저 인증이 필요한 기능은 꼭 설정해주세요)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserLevelView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]

        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
                user_level = User.objects.get(id=int(user_pk)).level
                return Response({'level': user_level})
            except Exception as e:
                content = {
                    'message': "잘못된 토큰값이 들어왔습니다."
                }
                return Response(content)


class UserInfoView(APIView):
    permission_classes(IsAuthenticated, )

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
                userInfo = User.objects.filter(id=user_pk)
                jsonUserInfo = UserSerializer(userInfo, many=True).data
                return Response(jsonUserInfo)
            except:
                content = {
                    'message': "잘못된 토큰값이 들어왔습니다."
                }
                return Response(content)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    if request.method == 'POST':
        print('2')
        serializer = UserCreateSerializer(data=request.data)
        print('1')
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "ok", "code": 1}, status=status.HTTP_201_CREATED)
        else :
            return Response({"message": "error", "code": 0}, status=status.HTTP_400_BAD_REQUEST)

    # serializer = UserCreateSerializer(data=request.data)
    # if not serializer.is_valid(raise_exception=True):
    #     return Response({"message": "Request Body Error.", "code": 0}, status=status.HTTP_409_CONFLICT)
    #
    # check_id = User.objects.filter(user_id=serializer.validated_data['user_id']).first()
    # check_email = User.objects.filter(email=serializer.validated_data['email']).first()
    # if check_id is None and check_email is None:
    #     serializer.save()
    #     return Response({"message": "ok", "code": 1}, status=status.HTTP_201_CREATED)
    # if check_id is not None:
    #     print("id중복?")
    #     return Response({"message": "duplicate ID", "code": 2}, status=status.HTTP_409_CONFLICT)
    # if check_email is not None:
    #     print("email중복?")
    #     return Response({"message": "duplicate Email", "code": 3}, status=status.HTTP_409_CONFLICT)
