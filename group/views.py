from rest_framework import status
from rest_framework.response import Response
from .models import GroupManage, Group
from .serializers import GroupSerializer, GroupManageSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings
from account.models import User
from account.serializers import UserSerializer
from rest_framework.decorators import permission_classes
from django.http import Http404
from django.db.models import Q

class GroupListAPIView(APIView):
    permission_classes(IsAuthenticated, )

    def get_object(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]
        if token:
            try:
                user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
                return User.objects.filter(id=user_pk)
            except Exception as e:
                return Http404
        else:
            return Http404

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]
        if token:
            # try:
            user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
            userInfo = User.objects.get(id=user_pk)
            GroupInfo = Group.objects.get(Q(group_master=userInfo) & Q(group_name=request.data["group_name"]))
            serializer = GroupSerializer(GroupInfo)
            return Response(serializer.data)
            # serializer = GroupSerializer(GroupInfo, many=True).data
            '''except Exception as e:
                content = {
                    'message': "왜 안되누"
                }
                return Response(content)'''
        else:
            content = {
                'message': "로그인 후 다시 시도해주세요"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class GroupManageListAPIView(APIView):
    def post(self, request):
        serializer = GroupManageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = GroupManageSerializer(GroupManage.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.shortcuts import get_object_or_404


class GroupDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Group, pk=pk)

    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, pk):
        group = self.get_object(pk)
        group.group_visible = request.data['group_visible']
        if request.data['description'] == '':
            serializer = GroupSerializer(group)
            group.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.data['description'] != '':
            group.description = request.data['description']
            serializer = GroupSerializer(group)
            group.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = GroupSerializer(group)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = self.get_object(pk)
        # 중간에 길드장과 일치하는 사용자인지 체크해야되는 함수가 필요한가?
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupManageDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(GroupManage, pk=pk)

    def get(self, request, pk):
        groupmanage = self.get_object(pk)
        serializer = GroupSerializer(groupmanage)
        return Response(serializer.data)

    def put(self, request, pk):
        groupmanage = self.get_object(pk)
        group = Group.objects.get(group_name=groupmanage.group_id)
        if group.group_master == request.data['user']:
            groupmanage.status = request.data['status']
            groupmanage.save()
            serializer = GroupManageSerializer(groupmanage)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = GroupManageSerializer(groupmanage)
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        groupmanage = self.get_object(pk)
        groupmanage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
