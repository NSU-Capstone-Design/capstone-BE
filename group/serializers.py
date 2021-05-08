from rest_framework import serializers
from group.models import Group, GroupManage
from account.models import User
from account.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'group_name',
            'introduce',
            'group_visible',
            'group_master',
        ]


class GroupManageSerializer(serializers.ModelSerializer):
    member = UserSerializer()

    class Meta:
        model = GroupManage
        fields = [
            'group_id',
            'member',
            'status'
        ]
