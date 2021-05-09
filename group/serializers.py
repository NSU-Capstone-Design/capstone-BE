from rest_framework import serializers
from group.models import Group, GroupManage
from account.models import User
from account.serializers import UserSerializer


class GroupMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'nickname',
        ]


class GroupSerializer(serializers.ModelSerializer):
    group_master = GroupMasterSerializer()

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
    group_id = GroupSerializer()

    class Meta:
        model = GroupManage
        fields = [
            'group_id',
            'member',
            'status'
        ]
