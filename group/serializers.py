from rest_framework import serializers
from group.models import Group, GroupManage
from account.models import User
from account.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    group_master = UserSerializer()

    class Meta:
        model = Group
        fields = [
            'id',
            'group_name',
            'introduce',
            'group_visible',
            'group_master',
        ]

class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'group_name',
            'introduce',
            'group_visible',
            'group_master',
        ]

class GroupManageSerializer(serializers.ModelSerializer):
    member = UserSerializer()
    group_id = GroupSerializer()

    class Meta:
        model = GroupManage
        fields = [
            'group_id',
            'member',
            'status',
        ]
