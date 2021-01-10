from rest_framework import serializers

from project.models import *

class GroupManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupManage
        fields = [
            'master',
            'description',
            'name'
        ]