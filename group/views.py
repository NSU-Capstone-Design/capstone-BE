from rest_framework import status
from rest_framework.response import Response
from .models import GroupManage, Group
from .serializers import GroupSerializer, GroupManageSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings
from account.models import User
from rest_framework.decorators import permission_classes
from django.db import IntegrityError


class GroupListAPIView(APIView):
    permission_classes(IsAuthenticated, )

    def get_object(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)[7:]
        if token:
            try:
                user_pk = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['user_id']
                return User.objects.get(id=user_pk)
            except Exception as e:
                return False
        else:
            return False

    def post(self, request):
        if self.get_object(request):
            userInfo = self.get_object(request)

            if userInfo.is_admin:
                group = {
                    'group_name': request.data['group_name'],
                    'introduce': request.data['introduce'],
                    'group_visible': request.data['group_visible'],
                    'group_master': userInfo.id
                }
                serializer = GroupSerializer(data=group)

                try:
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except IntegrityError as e:
                    if 'UNIQUE constraint' in e.args[0]:
                        content = {
                            "Errormsg" :
                                (userInfo.nickname + "님은 이미 '" +
                                group['group_name'] + "'(이)라는 그룹명을 가지고 있습니다.")
                        }
                        return Response(content,status=status.HTTP_400_BAD_REQUEST)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            content = {
                'message': "그룹 생성 권한이 없습니다."
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        content = {
            'message': "로그인 후 사용가능합니다."
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if self.get_object(request):
            userInfo = self.get_object(request)
            if userInfo.expert_user:
                groupInfo = Group.objects.filter(group_master=userInfo)
                serializer = GroupSerializer(groupInfo, many=True)
                data = [
                    {'isExpertUser': userInfo.expert_user},
                    serializer.data
                ]
                return Response(data)
            groupInfo = GroupManage.objects.filter(member = userInfo)
            groupList = []
            for x in groupInfo:
                groupList.append(x.group_id)
            serializer = GroupSerializer(groupList, many=True)
            data = [
                    {'isExpertUser': userInfo.expert_user},
                    serializer.data
            ]
            return Response(data)
        else:
            content = {
                'message': "로그인 안함"
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class GroupDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Group, pk=pk)

    def get(self, request, pk):
        group = self.get_object(pk)
        memberList = GroupManage.objects.filter(group_id=group)
        print(memberList)
        serializer = GroupSerializer(group)
        print(serializer.data)
        serializer_m = GroupManageSerializer(memberList, many=True)
        data = [
            serializer.data,
            serializer_m.data
        ]
        print(data)
        return Response(data)

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
