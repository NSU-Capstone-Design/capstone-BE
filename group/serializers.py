from rest_framework import serializers
from group.models import Group, GroupManage
from account.models import User

class GroupSerializer(serializers.ModelSerializer):
    group_master = serializers.ReadOnlyField(source='group_master.nickname')

    class Meta:
        model = Group
        fields = [
            'group_name',
            'introduce',
            'group_visible',
            'group_master',
        ]

class GroupManageSerializer(serializers.ModelSerializer):
    member = serializers.ReadOnlyField(source='member.nickname')
    class Meta:
        model = GroupManage
        fields = [
            'group_id',
            'member',
            'status'
        ]