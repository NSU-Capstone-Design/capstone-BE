from rest_framework import serializers
from group.models import Group, GroupManage
from account.models import User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'group_name',
            'introduce',
            'group_visible',
            'group_master',
        ]

class GroupManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupManage
        fields = [
            'group_id',
            'member',
            'status'
        ]